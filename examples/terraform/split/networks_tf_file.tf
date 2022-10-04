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
resource "aws_subnet" "PublicSubnet1" {
  vpc_id     = aws_vpc.CustomVPC.id
  cidr_block = "10.0.0.0/24"
}
resource "aws_subnet" "PublicSubnet2" {
  vpc_id     = aws_vpc.CustomVPC.id
  cidr_block = "10.0.1.0/24"
}