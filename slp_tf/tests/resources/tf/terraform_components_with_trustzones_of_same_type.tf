resource "aws_vpc" "CustomVPC" {
  cidr_block  = "10.0.0.0/16"
}

resource "aws_rds_cluster" "RDSCluster" {
}