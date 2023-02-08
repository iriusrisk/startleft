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
  resource "aws_security_group" "VPCssmSecurityGroup" {
    vpc_id        = aws_vpc.CustomVPC.id

    egress {
      from_port   = 0
      to_port     = 0
      protocol    = "-1"
      cidr_blocks = ["0.0.0.0/0"]
      description = "Allow all outbound traffic by default"
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
      aws_subnet.PrivateSubnet1.id
    ]
  
    private_dns_enabled = true
  }