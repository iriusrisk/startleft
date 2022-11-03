variable "aws_profile" {
  description = "The AWS-CLI profile for the account to create resources in."
}
variable "aws_region" {
  description = "The AWS region to create resources in."
}
variable "instance_name" {
  description = "The instance name."
}
variable "type" {
  description = "A type to describe the environment we're creating, prod/eval/internal."
}
variable "bastion_host_cidrs" {
  description = "The IP ranges of bastion hosts to ssh web server instances."
  type = list
}
variable "iriusrisk_version" {
  description = "iriusrisk version"
}
variable "startleft_version" {
  description = "startleft version"
}
variable "certificate_arn" {
  description = "certificate arn"
}
variable "iam_instance_profile_arn" {
  description = "iam_instance_profile arn"
}
variable "vpc_cidr" {
  description = "The IP range to attribute to the virtual network."
}
variable "public_subnet_cidrs" {
  description = "The IP ranges to use for the public subnets in your VPC."
  type = list
}
variable "private_subnet_cidrs" {
  description = "The IP ranges to use for the private subnets in your VPC."
  type = list
}
variable "database_subnet_cidrs" {
  description = "The IP ranges to use for the database subnets in your VPC."
  type = list
}
variable "availability_zones" {
  description = "The AWS availability zones to create subnets in."
  type = list
}
variable "rds_instance_type" {
  description = "rds instance type"
}
variable "rds_engine_version" {
  description = "rds engine version"
}
variable "rds_family" {
  description = "rds family"
}
variable "major_engine_version" {
  description = "major_engine_version"
}
variable "dbname" {
  description = "postgresql database name"
}
variable "dbuser" {
  description = "postgresql user"
}
variable "dbpassword" {
  description = "postgresql passwrod"
}
variable "ec2_instance_type" {
  description = "instance type"
}
variable "key_name" {
  description = "instance asscessing key"
}
variable "min_size" {
  description = "min_size"
}
variable "max_size" {
  description = "max_size"
}
variable "desired_capacity" {
  description = "desired_capacity"
}

### cloudflare
variable "cloudflare_zone_id" {
  description = "cloudflare_zone_id"
  default = ""
}
variable "cloudflare_email" {
  description = "cloudflare_email"
  default = ""
}
variable "cloudflare_api_key" {
  description = "cloudflare_api_key"
  default = ""
}
variable "cloudflare_token" {
  description = "cloudflare token replaces email+api_key"
  default = ""
}
