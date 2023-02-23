resource "aws_security_group" "this" {
	ingress {
    	cidr_blocks      = ["0.0.0.0/0"]
  	}
}

resource "aws_security_group" "this" {
    egress {
    	cidr_blocks      = ["0.0.0.0/0"]
  	}
}