resource "aws_resource_a" "resource_a" {
}
resource "aws_resource_b" "resource_b" {
	vpc_id     = aws_resource_a.resource_a.id
}