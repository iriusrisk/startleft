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