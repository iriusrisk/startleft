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
resource "aws_lambda_function" "basic_lambda" {
  function_name = "lambda_function_name"
  role          = aws_iam_role.iam_for_basic_lambda.arn
}
resource "aws_lambda_event_source_mapping" "basic_dynamodb_event" {
  event_source_arn  = aws_dynamodb_table.basic_dynamodb_table.stream_arn
  function_name     = aws_lambda_function.basic_lambda.arn
}