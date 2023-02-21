resource "aws_db_instance" "mysql" {}

resource "aws_db_instance" "mysql-secret" {}

resource "aws_rds_cluster" "aurora-cluster-demo" {}