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
resource "aws_subnet" "PublicSubnet1" {
  vpc_id     = aws_vpc.CustomVPC.id
  cidr_block = "10.0.0.0/24"
}
resource "aws_security_group" "ServiceLBSecurityGroup" {
  vpc_id        = aws_vpc.CustomVPC.id
}
resource "aws_security_group" "CanarySecurityGroup" {
  vpc_id        = aws_vpc.CustomVPC.id
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
resource "aws_lb" "ServiceLB" {
  load_balancer_type          = "application"
  internal                    = true
  enable_deletion_protection  = false
  security_groups             = [aws_security_group.ServiceLBSecurityGroup.id]
  subnets                     = [aws_subnet.PrivateSubnet1.id]
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
    subnet_ids = [aws_subnet.PublicSubnet1.id]
    security_group_ids = [aws_security_group.CanarySecurityGroup.id]
  }
}

