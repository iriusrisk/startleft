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