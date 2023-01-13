resource "aws_security_group" "this" {
	ingress {
    	cidr_blocks      = ["0.0.0.0/0"]
  	}
    egress {
    	cidr_blocks      = ["192.168.0.1/0"]
  	}
}