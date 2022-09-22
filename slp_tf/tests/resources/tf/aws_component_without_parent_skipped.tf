resource "aws_skipped_with_parent" "Skipped_with_parent" {
  name = "aws-skipped-with-parent"
}

resource "aws_skipped_no_parent" "Skipped_no_parent" {
  name = "aws-skipped-no-parent"
}

resource "aws_control" "Control_component" {
  name = "aws-control"
}