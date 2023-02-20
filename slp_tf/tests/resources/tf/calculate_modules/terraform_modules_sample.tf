resource "aws_cloudwatch_metric_alarm" "cloudwatch_metric_alarm_1" {
  alarm_name                = "terraform-test-foobar5"
  comparison_operator       = "GreaterThanOrEqualToThreshold"
  evaluation_periods        = "2"
  metric_name               = "CPUUtilization"
  namespace                 = "AWS/EC2"
  period                    = "120"
  statistic                 = "Average"
  threshold                 = "80"
  alarm_description         = "This metric monitors ec2 cpu utilization"
  insufficient_data_actions = []
}

resource "aws_acm_certificate" "acm_certificate" {
  domain_name       = "example.com"
  validation_method = "DNS"

  tags = {
    Environment = "test"
  }

  lifecycle {
    create_before_destroy = true
  }
}

module "db23test" {
  source  = "terraform-aws-modules/rds/aws"
  version = "4.3.0"

  identifier = "iriusrisk-${var.instance_name}-rds"

  engine               = "postgres"
  engine_version       = var.rds_engine_version
  family               = var.rds_family
  major_engine_version = var.major_engine_version
  instance_class       = var.rds_instance_type

  allocated_storage     = 16
  max_allocated_storage = 512
  storage_encrypted     = false

  db_name                = var.dbname
  username               = var.dbuser
  password               = var.dbpassword
  create_random_password = false

  create_db_subnet_group      = true
  db_subnet_group_description = "Subnets for manual RDS"
  db_subnet_group_name        = "${var.instance_name}-rds-subnets"

  multi_az                   = false
  auto_minor_version_upgrade = false

  subnet_ids             = module.vpc.private_subnets
  vpc_security_group_ids = [aws_security_group.rds.id]

  backup_retention_period = 7
  skip_final_snapshot     = true
  deletion_protection     = false

  performance_insights_enabled          = false
  performance_insights_retention_period = 10
  create_monitoring_role                = false
  monitoring_interval                   = 0

  parameter_group_name = "${var.instance_name}-postgres11-ssl"
  parameters           = [
    {
      name  = "rds.force_ssl"
      value = 1
    }
  ]

  tags = {
    Name = "iriusrisk-${var.instance_name}-rds"
    type = var.type
  }
}
