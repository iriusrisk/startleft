variable "vpcCidrblock" {
  type    = list
  default = ["10.0.0.0/16"]
}
variable "ingressCidrblock" {
  type    = list
  default = ["0.0.0.0/0"]
}


resource "aws_security_group" "VPCssmSecurityGroup" {
  vpc_id        = aws_vpc.CustomVPC.id

  ingress {
    cidr_blocks = var.vpcCidrblock
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    description = "from CustomVPC:443"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic by default"
  }
}
resource "aws_security_group" "VPCssmmessagesSecurityGroup" {
  vpc_id        = aws_vpc.CustomVPC.id

  ingress {
    cidr_blocks = var.vpcCidrblock
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    description = "from CustomVPC:443"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic by default"
  }
}
resource "aws_security_group" "VPCmonitoringSecurityGroup" {
  vpc_id        = aws_vpc.CustomVPC.id

  ingress {
    cidr_blocks = var.vpcCidrblock
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    description = "from CustomVPC:443"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = var.ingressCidrblock
    description = "Allow all outbound traffic by default"
  }
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
resource "aws_security_group" "CanarySecurityGroup" {
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
resource "aws_security_group_rule" "CanarySecurityGroupEgresstoServiceLBSecurityGroup" {
  type                      = "egress"
  from_port                 = 443
  to_port                   = 443
  protocol                  = "tcp"
  security_group_id         = aws_security_group.CanarySecurityGroup.id
  source_security_group_id  = aws_security_group.ServiceLBSecurityGroup.id
  description               = "to ServiceLBSecurityGroup:443"
}
resource "aws_security_group_rule" "ServiceLBSecurityGroupIngressfromCanarySecurityGroup" {
  type                      = "ingress"
  from_port                 = 443
  to_port                   = 443
  protocol                  = "tcp"
  security_group_id         = aws_security_group.ServiceLBSecurityGroup.id
  source_security_group_id  = aws_security_group.CanarySecurityGroup.id
  description               = "from CanarySecurityGroup:443"
}

resource "aws_vpc_endpoint" "VPCssm" {
  vpc_id            = aws_vpc.CustomVPC.id
  service_name      = "com.amazonaws.us-west-2.ssm"
  vpc_endpoint_type = "Interface"

  security_group_ids = [
    aws_security_group.VPCssmSecurityGroup.id,
  ]
  subnet_ids         = [
    aws_subnet.PrivateSubnet1.id,
    aws_subnet.PrivateSubnet2.id
  ]

  private_dns_enabled = true
}
resource "aws_vpc_endpoint" "VPCssmmessages" {
  vpc_id            = aws_vpc.CustomVPC.id
  service_name      = "com.amazonaws.us-west-2.ssmmessages"
  vpc_endpoint_type = "Interface"

  security_group_ids = [
    aws_security_group.VPCssmmessagesSecurityGroup.id,
  ]

  private_dns_enabled = true

  subnet_ids = [
    aws_subnet.PrivateSubnet1.id,
    aws_subnet.PrivateSubnet2.id
  ]
}
resource "aws_vpc_endpoint" "VPCmonitoring" {
  vpc_id            = aws_vpc.CustomVPC.id
  service_name      = "com.amazonaws.us-west-2.monitoring"
  vpc_endpoint_type = "Interface"

  security_group_ids = [
    aws_security_group.VPCmonitoringSecurityGroup.id,
  ]

  private_dns_enabled = true

  subnet_ids = [
    aws_subnet.PrivateSubnet1.id,
    aws_subnet.PrivateSubnet2.id
  ]
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
    subnets = [aws_subnet.PrivateSubnet1.id, aws_subnet.PrivateSubnet2.id]
    security_groups = [aws_security_group.OutboundSecurityGroup.id]
  }
}

resource "aws_lb" "ServiceLB" {
  load_balancer_type          = "application"
  internal                    = true
  enable_deletion_protection  = false
  security_groups             = [aws_security_group.ServiceLBSecurityGroup.id]
  subnets                     = [aws_subnet.PrivateSubnet1.id, aws_subnet.PrivateSubnet2.id]
}

resource "aws_synthetics_canary" "Canary" {
  name                 = "canary"
  artifact_s3_location = "s3://some-bucket/"
  execution_role_arn   = "some-role"
  handler              = "exports.handler"
  zip_file             = "test-fixtures/lambdatest.zip"
  runtime_version      = "syn-1.0"

  schedule {
    expression = "rate(0 minute)"
  }
  vpc_config {
    subnet_ids = [aws_subnet.PublicSubnet1.id, aws_subnet.PublicSubnet2.id]
    security_group_ids = [aws_security_group.CanarySecurityGroup.id]
  }
}