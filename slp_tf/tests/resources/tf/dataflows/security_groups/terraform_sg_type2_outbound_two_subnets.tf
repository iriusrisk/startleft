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