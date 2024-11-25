provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile
}

### vpc
module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "3.14.0"

  name            = "${var.instance_name}-VPC"
  cidr            = var.vpc_cidr
  azs             = var.availability_zones
  public_subnets  = var.public_subnet_cidrs
  private_subnets = var.private_subnet_cidrs
  #  database_subnets = var.database_subnet_cidrs

  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = {
    type = var.type
  }
}

module "alb" {
  source  = "terraform-aws-modules/alb/aws"
  version = "7.0.0"

  name = "${var.instance_name}-ALB"

  load_balancer_type = "application"

  vpc_id          = module.vpc.vpc_id
  subnets         = module.vpc.public_subnets
  security_groups = [aws_security_group.alb.id]

  enable_deletion_protection = false
  idle_timeout               = 900

  target_groups = [
    {
      name             = "${var.instance_name}-TG"
      backend_protocol = "HTTP"
      backend_port     = 8080
      target_type      = "instance"

      health_check = {
        healthy_threshold   = 4
        unhealthy_threshold = 2
        timeout             = 5
        interval            = 20
        path                = "/health"
      }

      stickiness = {
        type            = "lb_cookie"
        cookie_duration = 600
      }

      deregistration_delay          = 30
      load_balancing_algorithm_type = "round_robin"
    }
  ]

  http_tcp_listeners = [
    {
      port        = 80
      protocol    = "HTTP"
      action_type = "redirect"
      redirect    = {
        port        = "443"
        protocol    = "HTTPS"
        status_code = "HTTP_302"
      }
    }
  ]

  https_listeners = [
    {
      port               = 443
      protocol           = "HTTPS"
      target_group_index = 0
      certificate_arn    = var.certificate_arn
    }
  ]

  tags = {
    Name = "${var.instance_name}-ALB"
    type = var.type
  }
}

module "db" {
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
  #maintenance_window              = "Mon:00:00-Mon:03:00"
  #backup_window                   = "03:00-06:00"
  #enabled_cloudwatch_logs_exports = ["postgresql", "upgrade"]

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

data "aws_ami" "iriusrisk_ha" {
  most_recent = true
  owners      = ["123456789012"]

  filter {
    name   = "name"
    values = ["IriusRisk_HA_${var.iriusrisk_version}*"]
  }
}

data "template_file" "user_data" {
  template = "${file("${path.module}/templates/user_data.sh")}"

  vars = {
    aws_region        = var.aws_region
    instance_name     = var.instance_name
    iriusrisk_version = var.iriusrisk_version
    startleft_version = var.startleft_version
    dbname            = var.dbname
    dbuser            = var.dbuser
    dbpassword        = var.dbpassword
    rds_endpoint      = module.db.db_instance_address
  }
}

resource "aws_cloudwatch_metric_alarm" "cloudwatch_alarm_up" {
  alarm_name          = "${var.instance_name}-CPUUtilization-above-70"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 300
  statistic           = "Average"
  threshold           = 70

  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.asg.name
  }

  alarm_description = "Scale-up if CPU > 70% for 5 minutes"
  alarm_actions     = [aws_autoscaling_policy.scaling_up.arn]
}
