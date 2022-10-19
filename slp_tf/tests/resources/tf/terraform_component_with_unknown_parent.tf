resource "aws_internet_gateway" "InterneteGateway" {}
resource "aws_instance" "E2CINSTANCE" {}
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