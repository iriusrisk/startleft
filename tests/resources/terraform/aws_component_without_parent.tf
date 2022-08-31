resource "aws_skipped_with_parent" "Skipped_with_parent" {
  name = "aws-skipped-with-parent"
}

resource "aws_component_without_parent" "Component_without_parent" {
  name = "aws-component-without-parent"
}

resource "aws_control" "Control_component" {
  name = "aws-control"
}