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

resource "aws_cloudwatch_metric_alarm" "cloudwatch_metric_alarm_2" {
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

resource "aws_acm_certificate" "acm_certificate_1" {
  domain_name       = "example.com"
  validation_method = "DNS"

  tags = {
    Environment = "test"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_acm_certificate" "acm_certificate_2" {
  domain_name       = "example.com"
  validation_method = "DNS"

  tags = {
    Environment = "test"
  }

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_kms_key" "kms_key_1" {
  description             = "KMS key 1"
  deletion_window_in_days = 10
}

resource "aws_kms_key" "kms_key_2" {
  description             = "KMS key 1"
  deletion_window_in_days = 10
}

resource "aws_cloudwatch_log_group" "cloudwatch_log_group_1" {
  name = "Yada"

  tags = {
    Environment = "production"
    Application = "serviceA"
  }
}

resource "aws_cloudwatch_log_group" "cloudwatch_log_group_2" {
  name = "Yada"

  tags = {
    Environment = "production"
    Application = "serviceA"
  }
}

resource "aws_secretsmanager_secret" "secretsmanager_secret_1" {
  name = "example"
}

resource "aws_secretsmanager_secret" "secretsmanager_secret_2" {
  name = "example"
}

resource "aws_ssm_parameter" "ssm_parameter" {
  name  = "foo"
  type  = "String"
  value = "bar"
}

resource "aws_ssm_document" "ssm_document" {
  name          = "test_document"
  document_type = "Command"

  content = <<DOC
  {
    "schemaVersion": "1.2",
    "description": "Check ip configuration of a Linux instance.",
    "parameters": {

    },
    "runtimeConfig": {
      "aws:runShellScript": {
        "properties": [
          {
            "id": "0.aws:runShellScript",
            "runCommand": ["ifconfig"]
          }
        ]
      }
    }
  }
DOC
}

resource "aws_api_gateway_api_key" "api_gateway_api_key" {
  name = "demo"
}

resource "aws_api_gateway_client_certificate" "api_gateway_client_certificate" {
  description = "My client certificate"
}

resource "aws_athena_workgroup" "athena_workgroup" {
  name = "example"

  configuration {
    result_configuration {
      encryption_configuration {
        encryption_option = "SSE_KMS"
        kms_key_arn       = aws_kms_key.test.arn
      }
    }
  }
}

resource "aws_athena_database" "athena_database" {
  name   = "users"
  bucket = aws_s3_bucket.hoge.id
}

resource "aws_mq_broker" "mq_broker" {
  broker_name = "example"

  configuration {
    id       = aws_mq_configuration.test.id
    revision = aws_mq_configuration.test.latest_revision
  }

  engine_type        = "ActiveMQ"
  engine_version     = "5.15.9"
  host_instance_type = "mq.t2.micro"
  security_groups    = [aws_security_group.test.id]

  user {
    username = "ExampleUser"
    password = "MindTheGap"
  }
}

resource "aws_mq_configuration" "mq_configuration" {
  description    = "Example Configuration"
  name           = "example"
  engine_type    = "ActiveMQ"
  engine_version = "5.15.0"

  data = <<DATA
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<broker xmlns="http://activemq.apache.org/schema/core">
  <plugins>
    <forcePersistencyModeBrokerPlugin persistenceFlag="true"/>
    <statisticsBrokerPlugin/>
    <timeStampingBrokerPlugin ttlCeiling="86400000" zeroExpirationOverride="86400000"/>
  </plugins>
</broker>
DATA
}

resource "aws_cloudfront_origin_access_identity" "cloudfront_origin_access_identity" {
  comment = "Some comment"
}

resource "aws_cloudfront_public_key" "cloudfront_public_key" {
  comment     = "test public key"
  encoded_key = file("public_key.pem")
  name        = "test_key"
}

resource "aws_config_config_rule" "config_config_rule" {
  name = "example"

  source {
    owner             = "AWS"
    source_identifier = "S3_BUCKET_VERSIONING_ENABLED"
  }

  depends_on = [aws_config_configuration_recorder.foo]
}

resource "aws_config_configuration_recorder" "config_configuration_recorder" {
  name     = "example"
  role_arn = aws_iam_role.r.arn
}

resource "aws_ecr_repository" "ecr_repository" {
  name = "bar"
}

resource "aws_ecr_lifecycle_policy" "ecr_lifecycle_policy" {
  repository = aws_ecr_repository.foo.name

  policy = <<EOF
{
    "rules": [
        {
            "rulePriority": 1,
            "description": "Expire images older than 14 days",
            "selection": {
                "tagStatus": "untagged",
                "countType": "sinceImagePushed",
                "countUnit": "days",
                "countNumber": 14
            },
            "action": {
                "type": "expire"
            }
        }
    ]
}
EOF
}

resource "aws_elasticache_user" "elasticache_user" {
  user_id       = "testUserId"
  user_name     = "testUserName"
  access_string = "on ~app::* -@all +@read +@hash +@bitmap +@geo -setbit -bitfield -hset -hsetnx -hmset -hincrby -hincrbyfloat -hdel -bitop -geoadd -georadius -georadiusbymember"
  engine        = "REDIS"
  passwords     = ["password123456789"]
}

resource "aws_elasticache_user_group" "elasticache_user_group" {
  engine        = "REDIS"
  user_group_id = "userGroupId"
  user_ids      = [aws_elasticache_user.elasticache_user.user_id]
}

resource "aws_guardduty_detector" "guardduty_detector_1" {
  enable = true
}

resource "aws_guardduty_detector" "guardduty_detector_2" {
  provider = aws.dev

  enable = true
}

resource "aws_inspector_resource_group" "inspector_resource_group" {
  tags = {
    Name = "foo"
    Env  = "bar"
  }
}

resource "aws_inspector_assessment_target" "inspector_assessment_target" {
  name               = "assessment target"
  resource_group_arn = aws_inspector_resource_group.inspector_resource_group.arn
}

resource "aws_macie2_account" "macie2_account" {}

resource "aws_macie2_member" "macie2_member" {
  account_id                            = "AWS ACCOUNT ID"
  email                                 = "EMAIL"
  invite                                = true
  invitation_message                    = "Message of the invitation"
  invitation_disable_email_notification = true
  depends_on                            = [aws_macie2_account.macie2_account]
}

resource "aws_ses_receipt_filter" "ses_receipt_filter" {
  name   = "block-spammer"
  cidr   = "10.10.10.10"
  policy = "Block"
}

resource "aws_ses_receipt_rule" "ses_receipt_rule" {
  name          = "store"
  rule_set_name = "default-rule-set"
  recipients    = ["karen@example.com"]
  enabled       = true
  scan_enabled  = true

  add_header_action {
    header_name  = "Custom-Header"
    header_value = "Added by SES"
    position     = 1
  }

  s3_action {
    bucket_name = "emails"
    position    = 2
  }
}

resource "aws_sns_topic" "sns_topic" {
  name = "user-updates-topic"
}

resource "aws_sns_topic_subscription" "sns_topic_subscription" {
  topic_arn = "arn:aws:sns:us-west-2:432981146916:user-updates-topic"
  protocol  = "sqs"
  endpoint  = "arn:aws:sqs:us-west-2:432981146916:terraform-queue-too"
}

resource "aws_waf_ipset" "waf_ipset" {
  name = "tfIPSet"

  ip_set_descriptors {
    type  = "IPV4"
    value = "192.0.7.0/24"
  }
}

resource "aws_waf_rule" "waf_rule" {
  depends_on  = [aws_waf_ipset.waf_ipset]
  name        = "tfWAFRule"
  metric_name = "tfWAFRule"

  predicates {
    data_id = aws_waf_ipset.waf_ipset.id
    negated = false
    type    = "IPMatch"
  }
}

resource "aws_kinesis_analytics_application" "kinesis_analytics_application_1" {
  name = "kinesis-analytics-application-test"

  inputs {
    name_prefix = "test_prefix"

    kinesis_stream {
      resource_arn = aws_kinesis_stream.test_stream.arn
      role_arn     = aws_iam_role.test.arn
    }

    parallelism {
      count = 1
    }

    schema {
      record_columns {
        mapping  = "$.test"
        name     = "test"
        sql_type = "VARCHAR(8)"
      }

      record_encoding = "UTF-8"

      record_format {
        mapping_parameters {
          json {
            record_row_path = "$"
          }
        }
      }
    }
  }
}

resource "aws_kinesis_analytics_application" "kinesis_analytics_application_2" {
  name = "kinesis-analytics-application-test"

  inputs {
    name_prefix = "test_prefix"

    kinesis_stream {
      resource_arn = aws_kinesis_stream.test_stream.arn
      role_arn     = aws_iam_role.test.arn
    }

    parallelism {
      count = 1
    }

    schema {
      record_columns {
        mapping  = "$.test"
        name     = "test"
        sql_type = "VARCHAR(8)"
      }

      record_encoding = "UTF-8"

      record_format {
        mapping_parameters {
          json {
            record_row_path = "$"
          }
        }
      }
    }
  }
}

resource "aws_kinesis_stream" "kinesis_stream" {
  name        = "example-stream"
  shard_count = 1
}

resource "aws_kinesis_stream_consumer" "kinesis_stream_consumer" {
  name       = "example-consumer"
  stream_arn = aws_kinesis_stream.kinesis_stream.arn
}

resource "aws_kinesis_firehose_delivery_stream" "kinesis_firehose_delivery_stream_1" {
  name        = "terraform-kinesis-firehose-extended-s3-test-stream"
  destination = "extended_s3"

  extended_s3_configuration {
    role_arn   = aws_iam_role.firehose_role.arn
    bucket_arn = aws_s3_bucket.bucket.arn

    processing_configuration {
      enabled = "true"

      processors {
        type = "Lambda"

        parameters {
          parameter_name  = "LambdaArn"
          parameter_value = "${aws_lambda_function.lambda_processor.arn}:$LATEST"
        }
      }
    }
  }
}

resource "aws_kinesis_firehose_delivery_stream" "kinesis_firehose_delivery_stream_2" {
  name        = "terraform-kinesis-firehose-extended-s3-test-stream"
  destination = "extended_s3"

  extended_s3_configuration {
    role_arn   = aws_iam_role.firehose_role.arn
    bucket_arn = aws_s3_bucket.bucket.arn

    processing_configuration {
      enabled = "true"

      processors {
        type = "Lambda"

        parameters {
          parameter_name  = "LambdaArn"
          parameter_value = "${aws_lambda_function.lambda_processor.arn}:$LATEST"
        }
      }
    }
  }
}
