# VPC ENDPOINTS FOR SSM
provider "aws" {
  profile = var.profile
  region  = var.region
}

data "aws_vpc" "selected" {
  id = var.vpc_id
}
data "aws_availability_zones" "available" {}

locals {
  default_subnet_cidrs = ["${cidrhost(data.aws_vpc.selected.cidr_block, -128)}/26", "${cidrhost(data.aws_vpc.selected.cidr_block, -64)}/26"]
  selected_subnet_cidrs = coalescelist(var.subnet_cidrs, local.default_subnet_cidrs)
}

variable "profile" {
  description = "AWS Profile"
  default     = "default"
}
variable "region" {
  description = "AWS region"
  default     = "ap-south-1"
}
variable "vpc_id" {
  description = "AWS VPC ID"
  default = ["0.0.0.0/0"]
}
variable "subnet_cidrs" {
  description = "AWS Subnet CIDR ranges"
  type = "list"
  default = []
}

resource "aws_vpc_endpoint" "ssm" {
  vpc_id            = data.aws_vpc.selected.id
  service_name      = "com.amazonaws.${var.region}.ssm"
  vpc_endpoint_type = "Interface"

  private_dns_enabled = true
}
resource "aws_vpc_endpoint" "ssm_messages" {
  vpc_id            = data.aws_vpc.selected.id
  service_name      = "com.amazonaws.${var.region}.ssmmessages"
  vpc_endpoint_type = "Interface"

  private_dns_enabled = true
}
resource "aws_vpc_endpoint" "ecr" {
  vpc_id            = data.aws_vpc.selected.id
  service_name      = "com.amazonaws.${var.region}.ecr.dkr"
  vpc_endpoint_type = "Interface"

  private_dns_enabled = true
}
resource "aws_vpc_endpoint" "dynamodb" {
  vpc_id            = data.aws_vpc.selected.id
  service_name      = "com.amazonaws.${var.region}.dynamodb"
  vpc_endpoint_type = "Interface"

  private_dns_enabled = true
}
resource "aws_vpc_endpoint" "s3" {
  vpc_id            = data.aws_vpc.selected.id
  service_name      = "com.amazonaws.${var.region}.s3"
  vpc_endpoint_type = "Interface"

  private_dns_enabled = true
}
