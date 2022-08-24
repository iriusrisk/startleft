resource "aws_s3_bucket" "log_bucket_deprecated" {
  bucket = "my-tf-log-bucket"
  acl    = "log-delivery-write"
}
resource "aws_s3_bucket" "bucket_deprecated" {
  bucket = "my-tf-test-bucket"
  acl    = "private"

  logging {
    target_bucket = aws_s3_bucket.log_bucket_deprecated.id
    target_prefix = "log/"
  }
}
resource "aws_s3_bucket" "log_bucket" {
  bucket = "my-tf-log-bucket"
  acl    = "log-delivery-write"
}
resource "aws_s3_bucket" "bucket" {
  bucket = "my-tf-test-bucket"
  acl    = "private"
}
resource "aws_s3_bucket_logging" "logging" {
  bucket = aws_s3_bucket.bucket.id

  target_bucket = aws_s3_bucket.log_bucket.id
  target_prefix = "log/"
}

resource "aws_dynamodb_table" "basic_dynamodb_table" {
  name           = "GameScores"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "UserId"
  range_key      = "GameTitle"

  attribute {
    name = "UserId"
    type = "S"
  }
}

resource "aws_iam_role" "iam_for_basic_lambda" {
  name = "iam_for_basic_lambda"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_lambda_function" "basic_lambda" {
  function_name = "lambda_function_name"
  role          = aws_iam_role.iam_for_basic_lambda.arn
}
resource "aws_lambda_event_source_mapping" "basic_dynamodb_event" {
  event_source_arn  = aws_dynamodb_table.basic_dynamodb_table.stream_arn
  function_name     = aws_lambda_function.basic_lambda.arn

  destination_config {
    on_failure {
      destination_arn = aws_sqs_queue.failure_queue.arn
    }
  }
}
resource "aws_sqs_queue" "failure_queue" {
  name                      = "terraform-example-queue"
  delay_seconds             = 90
  max_message_size          = 2048
  message_retention_seconds = 86400
  receive_wait_time_seconds = 10
}

resource "aws_api_gateway_rest_api" "rest_api" {
  name = "auth-demo"
}
resource "aws_cognito_user_pool" "user_pool" {
  name = "mypool"
}
resource "aws_api_gateway_authorizer" "api_authorizer" {
  name                   = "demo"
  rest_api_id            = aws_api_gateway_rest_api.rest_api.id

  provider_arns = [aws_cognito_user_pool.user_pool.arn]
}
