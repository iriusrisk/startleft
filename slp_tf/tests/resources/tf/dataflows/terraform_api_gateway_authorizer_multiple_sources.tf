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
