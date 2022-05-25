data aws_caller_identity "current" {}

data aws_partition "current" {}

data "aws_cloudformation_export" "subnet_xyz" {
  name = "ExportsOutputRefVPCPrivateSubnet1SubnetXYZ"
}

data "aws_cloudformation_export" "subnet_abc" {
  name = "ExportsOutputRefVPCPrivateSubnet2SubnetABC"
}

data "aws_cloudformation_export" "custom_vpc" {
  name = "ExportsOutputRefCustomVPCBDGHIJK"
}

data "aws_cloudformation_export" "ecs_task_role" {
  name = "ECSTaskRoleF2ADB362"
}

data "aws_cloudformation_export" "ecs_execution_role" {
  name = "CounterServiceTaskDefExecutionRoleBBDDEEFF"
}

data "aws_cloudformation_export" "service_lb_security_group" {
  name = "ExportsOutputFnGetAttServiceLBSecurityGroupGroupId1122AABB"
}

resource "aws_vpc" "custom_vpc" {
  name = "custom_vpc"
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "private_subnet_1" {
  name = "private_subnet_1"

  vpc_id = aws_vpc.custom_vpc.id
  availability_zone = "Select"
  cidr_block = "10.0.2.0/24"
  map_public_ip_on_launch = false
}

resource "aws_subnet" "private_subnet_2" {
  name = "private_subnet_2"

  vpc_id = aws_vpc.custom_vpc.id
  availability_zone = "Select"
  cidr_block = "10.0.3.0/24"
  map_public_ip_on_launch = false
}

resource "aws_subnet" "public_subnet_1" {
  name = "public_subnet_1"

  vpc_id = aws_vpc.custom_vpc.id
  availability_zone = "Select"
  cidr_block = "10.0.0.0/24"
  map_public_ip_on_launch = false
}

resource "aws_subnet" "public_subnet_2" {
  name = "public_subnet_2"

  vpc_id = aws_vpc.custom_vpc.id
  availability_zone = "Select"
  cidr_block = "10.0.1.0/24"
  map_public_ip_on_launch = false
}

resource "aws_security_group" "vpc_ssm_security_group" {
  name = "vpc_ssm_security_group"
  description = "ECSFargateGoVPCStack/VPC/ssm/SecurityGroup"
  vpc_id = aws_vpc.custom_vpc.id

  egress {
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic by default"
    from_port = 0
    to_port   = 0
    protocol  = "-1"
  }

  ingress {
    cidr_blocks = [aws_vpc.custom_vpc.cidr_block]
    description = format("from ${aws_vpc.custom_vpc.cidr_block}:443")
    from_port = 443
    protocol  = "tcp"
    to_port   = 443

  }

  tags = {
    Name = "ECSFargateGoVPCStack/VPC"
  }

}

resource "aws_vpc_endpoint" "vpc_ssm" {
  name = "vpc_ssm"

  service_name = "com.amazonaws.us-east-1.ssm"
  vpc_id = aws_vpc.custom_vpc.id
  private_dns_enabled = true
  security_group_ids = [aws_security_group.vpc_ssm_security_group]
  subnet_ids = [aws_subnet.private_subnet_1.id, aws_subnet.private_subnet_2.id]
  vpc_endpoint_type = "Interface"
}

resource "aws_security_group" "vpc_ssm_messages_security_group" {
  name = "vpc_ssm_messages_security_group"
  description = "ECSFargateGoVPCStack/VPC/ssmmessages/SecurityGroup"
  vpc_id = aws_vpc.custom_vpc.id

  egress {
    cidr_blocks = ["0.0.0.0/0"]
    description = "Allow all outbound traffic by default"
    from_port = 0
    to_port   = 0
    protocol  = "-1"
  }

  ingress {
    cidr_blocks = [aws_vpc.custom_vpc.cidr_block]
    description = format("from ${aws_vpc.custom_vpc.cidr_block}:443")
    from_port = 443
    protocol  = "tcp"
    to_port   = 443

  }

  tags = {
    Name = "ECSFargateGoVPCStack/VPC"
  }

}

resource "aws_vpc_endpoint" "vpc_ssm_messages" {
  name = "vpc_ssm_messages"

  service_name = "com.amazonaws.us-east-1.ssmmessages"
  vpc_id = aws_vpc.custom_vpc.id
  private_dns_enabled = true
  security_group_ids = [aws_security_group.vpc_ssm_messages_security_group.id]
  subnet_ids = [data.aws_cloudformation_export.subnet_xyz.id, data.aws_cloudformation_export.subnet_abc.id]
  vpc_endpoint_type = "Interface"
}

resource "aws_security_group" "vpc_monitoring_security_group" {
  name = "vpc_monitoring_security_group"

  description = "ECSFargateGoVPCStack/VPC/monitoring/SecurityGroup"
  egress {
    description = "Allow all outbound traffic by default"
    cidr_blocks = ["0.0.0.0/0"]
    from_port = 0
    protocol  = "-1"
    to_port   = 0
  }
  ingress {
    description = format("from ${aws_vpc.custom_vpc.cidr_block}:443")
    cidr_blocks = [aws_vpc.custom_vpc.cidr_block]
    from_port = 443
    protocol  = "tcp"
    to_port   = 443
  }
  tags = {
    Name = "ECSFargateGoVPCStack/VPC"
  }
  vpc_id = aws_vpc.custom_vpc.id
}

resource "aws_vpc_endpoint" "vpc_monitoring" {
  name = "vpc_monitoring"

  service_name = "com.amazonaws.us-east-1.monitoring"
  vpc_id = aws_vpc.custom_vpc.id
  private_dns_enabled = true
  security_group_ids = [aws_security_group.vpc_monitoring_security_group.id]
  subnet_ids = [data.aws_cloudformation_export.subnet_xyz.id, data.aws_cloudformation_export.subnet_abc.id]
  vpc_endpoint_type = "Interface"
}

resource "aws_security_group" "outbound_security_group" {
  name = "outbound_security_group"
  description = "ECSFargateGoServiceStack/OutboundSecurityGroup"
  vpc_id = aws_vpc.custom_vpc.id

  egress {
    cidr_blocks = ["255.255.255.255/32"]
    description = "Disallow all traffic"
    from_port = 252
    to_port   = 86
    protocol  = "icmp"
  }

  tags = {
    Name = "ECSFargateGoVPCStack/VPC"
  }

}

resource "aws_security_group_rule" "outbound_security_group_ingress_service_lb_security_group" {
  name = "outbound_security_group_ingress_service_lb_security_group"

  type = "ingress"
  security_group_id = aws_security_group.outbound_security_group.id
  source_security_group_id = aws_security_group.service_lb_security_group.id
  protocol = "tcp"
  description = "Load balancer to target"
  from_port = 80
  to_port = 80
}

resource "aws_lb" "service_lb" {
  name = "service_lb"

  load_balancer_type = "application"
  enable_deletion_protection = false
  internal = "true"
  security_groups = [aws_security_group.service_lb_security_group.id]

  subnet_ids = [data.aws_cloudformation_export.subnet_xyz.id, data.aws_cloudformation_export.subnet_abc.id]
}

resource "aws_security_group" "service_lb_security_group" {
  name = "service_lb_security_group"
  description = "Automatically created Security Group for ELB ECSFargateGoServiceStackServiceLB"
  vpc_id = data.aws_cloudformation_export.custom_vpc
}

resource "aws_security_group_rule" "service_lb_security_group_egress_outbound_security_group" {
  name = "service_lb_security_group_egress_outbound_security_group"

  description = "Load balancer to target"
  type              = "egress"
  source_security_group_id = aws_security_group.outbound_security_group.id
  security_group_id = aws_security_group.service_lb_security_group.id
  from_port         = 80
  protocol          = "tcp"
  to_port           = 80
}

resource "aws_ecs_task_definition" "service_task_definition" {
  name = "service_task_definition"

  family = "ECSFargateGoServiceStackCounterServiceTaskDefAABBCCDD"
  cpu = "256"
  memory = "512"
  network_mode = "awsvpc"
  requires_compatibilities = ["FARGATE"]

  task_role_arn = data.aws_cloudformation_export.ecs_task_role.id
  execution_role_arn = data.aws_cloudformation_export.ecs_execution_role.id

  container_definitions = <<TASK_DEFINITION
  [
    {
      "Environment": [
        {
          "Name": "COUNTER_TABLE_NAME",
          "Value": {
            "Fn::ImportValue": "ECSFargateGoDataStack:ExportsOutputRefCounterTable0011223344556677"
          }
        }
      ],
      "Essential": true,
      "Image": {
        "Fn::Sub": "${data.aws_caller_identity.current.account_id}.dkr.ecr.us-east-1.${data.aws_partition.current.dns_suffix}/cdk-aa001122ds-container-assets-${data.aws_caller_identity.current.account_id}-us-east-1:00112233445566778899"
      },
      "LogConfiguration": {
        "LogDriver": "awslogs",
        "Options": {
          "awslogs-group": {
            "Ref": "CounterServiceTaskDefwebLogGroupAABBCCDD"
          },
          "awslogs-stream-prefix": "CounterService",
          "awslogs-region": "us-east-1"
        }
      },
      "Name": "web",
      "PortMappings": [
        {
          "ContainerPort": 80,
          "Protocol": "tcp"
        }
      ]
    }
  ]
  TASK_DEFINITION

}

resource "aws_ecs_service" "service" {
  name = "service"

  task_definition = aws_ecs_task_definition.service_task_definition
  network_configuration {
    assign_public_ip = "DISABLED"
    security_groups = [aws_security_group.outbound_security_group.id]
    subnets = [data.aws_cloudformation_export.subnet_xyz, data.aws_cloudformation_export.subnet_abc]
  }
}

resource "aws_security_group" "canary_security_group" {
  name = "canary_security_group"
  description = "ECSFargateGoCanaryStack/CanarySecurityGroup"

  vpc_id = data.aws_cloudformation_export.custom_vpc.id
}

resource "aws_security_group_rule" "canary_security_group_egress_to_service_lb_security_group" {
  name =  "canary_security_group_egress_to_service_lb_security_group"

  description = "to ECSFargateGoServiceStackServiceLBSecurityGroup:443"
  type              = "egress"
  from_port         = 443
  protocol          = "tcp"
  security_group_id = aws_security_group.canary_security_group.id
  source_security_group_id = data.aws_cloudformation_export.service_lb_security_group.id
  to_port           = 443
}

resource "aws_security_group_rule" "service_lb_security_group_ingress_from_canary_security_group" {
  name = service_lb_security_group_ingress_from_canary_security_group

  description = "from ECSFargateGoCanaryStackCanarySecurityGroup:443"
  type              = "ingress"
  from_port         = 443
  protocol          = "tcp"
  security_group_id = aws_security_group.canary_security_group.id
  source_security_group_id = aws_security_group.canary_security_group
  to_port           = 443
}

resource "aws_synthetics_canary" "canary" {
  name = "canary"

  vpc_config {
    security_group_ids = [aws_security_group.canary_security_group.id]
    subnet_ids = [data.aws_cloudformation_export.subnet_xyz.id, data.aws_cloudformation_export.subnet_abc.id]
  }
}