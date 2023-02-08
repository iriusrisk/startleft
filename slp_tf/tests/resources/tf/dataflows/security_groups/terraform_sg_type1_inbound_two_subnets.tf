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
  resource "aws_security_group" "VPCssmSecurityGroup" {
    vpc_id        = aws_vpc.CustomVPC.id
  
    ingress {
      cidr_blocks = var.vpcCidrblock
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      description = "from CustomVPC:443"
    }
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