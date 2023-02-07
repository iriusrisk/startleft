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