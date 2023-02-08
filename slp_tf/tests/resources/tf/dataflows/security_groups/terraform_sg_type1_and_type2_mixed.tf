variable "vpcCidrblock" {
  type    = list
  default = ["10.0.0.0/16"]
}
resource "aws_vpc" "CustomVPC" {
  cidr_block  = var.vpcCidrblock
}

resource "aws_subnet" "PrivateSubnet1" {
  vpc_id     = aws_vpc.CustomVPC.id
  cidr_block = "10.0.2.0/24"
}
resource "aws_subnet" "PrivateSubnet2" {
    vpc_id     = aws_vpc.CustomVPC.id
    cidr_block = "10.0.3.0/24"
}
resource "aws_security_group" "OutboundSecurityGroup" {
  vpc_id        = aws_vpc.CustomVPC.id

  egress {
    from_port   = 252
    to_port     = 86
    protocol    = "icmp"
    cidr_blocks = ["255.255.255.255/32"]
    description = "Disallow all traffic"
  }
}
resource "aws_security_group" "ServiceLBSecurityGroup" {
  vpc_id        = aws_vpc.CustomVPC.id
}

resource "aws_security_group_rule" "OutboundSecurityGroupIngressfromServiceLBSecurityGroup" {
  type                      = "ingress"
  from_port                 = 80
  to_port                   = 80
  protocol                  = "tcp"
  security_group_id         = aws_security_group.OutboundSecurityGroup.id
  source_security_group_id  = aws_security_group.ServiceLBSecurityGroup.id
  description               = "Load balancer to target"
}
resource "aws_security_group_rule" "ServiceLBSecurityGroupEgresstoOutboundSecurityGroup" {
  type                      = "egress"
  from_port                 = 80
  to_port                   = 80
  protocol                  = "tcp"
  security_group_id         = aws_security_group.ServiceLBSecurityGroup.id
  source_security_group_id  = aws_security_group.OutboundSecurityGroup.id
  description               = "Load balancer to target"
}
resource "aws_ecs_task_definition" "ServiceTaskDefinition" {
  family = "service"
  container_definitions = jsonencode([
    {
      name      = "first"
      image     = "service-first"
      cpu       = 10
      memory    = 512
      essential = true
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
        }
      ]
    },
    {
      name      = "second"
      image     = "service-second"
      cpu       = 10
      memory    = 256
      essential = true
      portMappings = [
        {
          containerPort = 443
          hostPort      = 443
        }
      ]
    }
  ])

  volume {
    name      = "service-storage"
    host_path = "/ecs/service-storage"
  }

  placement_constraints {
    type       = "memberOf"
    expression = "attribute:ecs.availability-zone in [us-west-2a, us-west-2b]"
  }
}
resource "aws_ecs_service" "Service" {
  name            = "service"
  task_definition = aws_ecs_task_definition.ServiceTaskDefinition.arn

  network_configuration {
    subnets = [aws_subnet.PrivateSubnet1.id]
    security_groups = [aws_security_group.OutboundSecurityGroup.id]
  }
}

resource "aws_lb" "ServiceLB" {
  load_balancer_type          = "application"
  internal                    = true
  enable_deletion_protection  = false
  security_groups             = [aws_security_group.ServiceLBSecurityGroup.id]
  subnets                     = [aws_subnet.PrivateSubnet1.id]
}