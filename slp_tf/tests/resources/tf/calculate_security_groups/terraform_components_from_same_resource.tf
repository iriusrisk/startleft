resource "aws_security_group" "test" {
  description = "Allow http to client host"
  vpc_id      = "myVPC"

  ingress {
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
    cidr_blocks      = ["52.30.97.44/32"]
  }

  egress {
    from_port        = 80
    to_port          = 80
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }
}

