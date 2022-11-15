from otm.otm.otm import Component
from slp_cft.slp_cft.parse.mapping.cft_path_ids_calculator import CloudformationPathIdsCalculator


def create_otm_component(component_data: {}) -> Component:
    return Component(**component_data)


def to_otm_components(components_data: []) -> [Component]:
    return [create_otm_component(data) for data in components_data]


SGS_COMPONENTS = to_otm_components([
    {
        'name': 'PrivateSubnet1',
        'type': 'empty-component',
        'source': {
            'Type': 'AWS::EC2::Subnet',
            'Properties': {
                'VpcId': {
                    'Ref': 'CustomVPC'
                },
                'AvailabilityZone': 'Select',
                'CidrBlock': '10.0.2.0/24',
                'MapPublicIpOnLaunch': 'false'
            },
            '_key': 'PrivateSubnet1'
        },
        'parent': '31401380-c6c5-41ad-a0d1-65d6ff93ebd9',
        'tags': [
            'AWS::EC2::Subnet'
        ],
        'id': '04fcb189-09f9-41d2-88f2-20c636b0adfc',
        'parent_type': 'component'
    },
    {
        'name': 'PrivateSubnet2',
        'type': 'empty-component',
        'source': {
            'Type': 'AWS::EC2::Subnet',
            'Properties': {
                'VpcId': {
                    'Ref': 'CustomVPC'
                },
                'AvailabilityZone': 'elect',
                'CidrBlock': '10.0.3.0/24',
                'MapPublicIpOnLaunch': 'false'
            },
            '_key': 'PrivateSubnet2'
        },
        'parent': '31401380-c6c5-41ad-a0d1-65d6ff93ebd9',
        'tags': [
            'AWS::EC2::Subnet'
        ],
        'id': '8f2c8747-641a-4a7e-8240-83e8e59d1ea7',
        'parent_type': 'component'
    },
    {
        'name': 'PublicSubnet1',
        'type': 'empty-component',
        'source': {
            'Type': 'AWS::EC2::Subnet',
            'Properties': {
                'VpcId': {
                    'Ref': 'CustomVPC'
                },
                'AvailabilityZone': 'Select',
                'CidrBlock': '10.0.0.0/24',
                'MapPublicIpOnLaunch': 'false'
            },
            '_key': 'PublicSubnet1'
        },
        'parent': '31401380-c6c5-41ad-a0d1-65d6ff93ebd9',
        'tags': [
            'AWS::EC2::Subnet'
        ],
        'id': 'b4085343-2934-4c4d-8148-67c1bf4cc070',
        'parent_type': 'component'
    },
    {
        'name': 'PublicSubnet2',
        'type': 'empty-component',
        'source': {
            'Type': 'AWS::EC2::Subnet',
            'Properties': {
                'VpcId': {
                    'Ref': 'CustomVPC'
                },
                'AvailabilityZone': 'Select',
                'CidrBlock': '10.0.1.0/24',
                'MapPublicIpOnLaunch': 'false'
            },
            '_key': 'PublicSubnet2'
        },
        'parent': '31401380-c6c5-41ad-a0d1-65d6ff93ebd9',
        'tags': [
            'AWS::EC2::Subnet'
        ],
        'id': 'f1d093a9-b0e7-4548-8e2f-b6d0f4a3fa26',
        'parent_type': 'component'
    },
    {
        'name': 'VPCssm',
        'type': 'empty-component',
        'source': {
            'Type': 'AWS::EC2::VPCEndpoint',
            'Properties': {
                'ServiceName': 'com.amazonaws.us-east-1.ssm',
                'VpcId': {
                    'Ref': 'CustomVPC'
                },
                'PrivateDnsEnabled': 'true',
                'SecurityGroupIds': [
                    {
                        'Fn::GetAtt': [
                            'VPCssmSecurityGroup',
                            'GroupId'
                        ]
                    }
                ],
                'SubnetIds': [
                    {
                        'Ref': 'PrivateSubnet1'
                    },
                    {
                        'Ref': 'PrivateSubnet2'
                    }
                ],
                'VpcEndpointType': 'Interface'
            },
            '_key': 'VPCssm',
            'altsource': True
        },
        'parent': '04fcb189-09f9-41d2-88f2-20c636b0adfc',
        'tags': [
            'AWS::EC2::VPCEndpoint'
        ],
        'id': '18c59d7c-acb7-4210-b060-4074a0ab012e',
        'parent_type': 'component'
    },
    {
        'name': 'VPCssm',
        'type': 'empty-component',
        'source': {
            'Type': 'AWS::EC2::VPCEndpoint',
            'Properties': {
                'ServiceName': 'com.amazonaws.us-east-1.ssm',
                'VpcId': {
                    'Ref': 'CustomVPC'
                },
                'PrivateDnsEnabled': 'true',
                'SecurityGroupIds': [
                    {
                        'Fn::GetAtt': [
                            'VPCssmSecurityGroup',
                            'GroupId'
                        ]
                    }
                ],
                'SubnetIds': [
                    {
                        'Ref': 'PrivateSubnet1'
                    },
                    {
                        'Ref': 'PrivateSubnet2'
                    }
                ],
                'VpcEndpointType': 'Interface'
            },
            '_key': 'VPCssm',
            'altsource': True
        },
        'parent': '8f2c8747-641a-4a7e-8240-83e8e59d1ea7',
        'tags': [
            'AWS::EC2::VPCEndpoint'
        ],
        'id': 'eed89218-8388-412f-b357-b4240c0e57fe',
        'parent_type': 'component'
    },
    {
        'name': 'VPCssmmessages',
        'type': 'empty-component',
        'source': {
            'Type': 'AWS::EC2::VPCEndpoint',
            'Properties': {
                'ServiceName': 'com.amazonaws.us-east-1.ssmmessages',
                'VpcId': {
                    'Ref': 'CustomVPC'
                },
                'PrivateDnsEnabled': 'true',
                'SecurityGroupIds': [
                    {
                        'Fn::GetAtt': [
                            'VPCssmmessagesSecurityGroup',
                            'GroupId'
                        ]
                    }
                ],
                'SubnetIds': [
                    {
                        'Ref': 'VPCPrivateSubnet1SubnetXYZ'
                    },
                    {
                        'Ref': 'VPCPrivateSubnet2SubnetABC'
                    }
                ],
                'VpcEndpointType': 'Interface'
            },
            '_key': 'VPCssmmessages',
            'altsource': True
        },
        'parent': '04fcb189-09f9-41d2-88f2-20c636b0adfc',
        'tags': [
            'AWS::EC2::VPCEndpoint'
        ],
        'id': 'ee00a4cf-39c2-4459-8c72-345d89320634',
        'parent_type': 'component'
    },
    {
        'name': 'VPCssmmessages',
        'type': 'empty-component',
        'source': {
            'Type': 'AWS::EC2::VPCEndpoint',
            'Properties': {
                'ServiceName': 'com.amazonaws.us-east-1.ssmmessages',
                'VpcId': {
                    'Ref': 'CustomVPC'
                },
                'PrivateDnsEnabled': 'true',
                'SecurityGroupIds': [
                    {
                        'Fn::GetAtt': [
                            'VPCssmmessagesSecurityGroup',
                            'GroupId'
                        ]
                    }
                ],
                'SubnetIds': [
                    {
                        'Ref': 'VPCPrivateSubnet1SubnetXYZ'
                    },
                    {
                        'Ref': 'VPCPrivateSubnet2SubnetABC'
                    }
                ],
                'VpcEndpointType': 'Interface'
            },
            '_key': 'VPCssmmessages',
            'altsource': True
        },
        'parent': '8f2c8747-641a-4a7e-8240-83e8e59d1ea7',
        'tags': [
            'AWS::EC2::VPCEndpoint'
        ],
        'id': '41aaf28a-2b7e-4c73-b6e7-c347f2006fdd',
        'parent_type': 'component'
    },
    {
        'name': 'VPCmonitoring',
        'type': 'empty-component',
        'source': {
            'Type': 'AWS::EC2::VPCEndpoint',
            'Properties': {
                'ServiceName': 'com.amazonaws.us-east-1.monitoring',
                'VpcId': {
                    'Ref': 'CustomVPC'
                },
                'PrivateDnsEnabled': 'true',
                'SecurityGroupIds': [
                    {
                        'Fn::GetAtt': [
                            'VPCmonitoringSecurityGroup',
                            'GroupId'
                        ]
                    }
                ],
                'SubnetIds': [
                    {
                        'Ref': 'VPCPrivateSubnet1SubnetXYZ'
                    },
                    {
                        'Ref': 'VPCPrivateSubnet2SubnetABC'
                    }
                ],
                'VpcEndpointType': 'Interface'
            },
            '_key': 'VPCmonitoring'
        },
        'parent': '04fcb189-09f9-41d2-88f2-20c636b0adfc',
        'tags': [
            'AWS::EC2::VPCEndpoint'
        ],
        'id': 'bda1120b-1e0e-430a-97f2-480d8953a3d7',
        'parent_type': 'component'
    },
    {
        'name': 'VPCmonitoring',
        'type': 'empty-component',
        'source': {
            'Type': 'AWS::EC2::VPCEndpoint',
            'Properties': {
                'ServiceName': 'com.amazonaws.us-east-1.monitoring',
                'VpcId': {
                    'Ref': 'CustomVPC'
                },
                'PrivateDnsEnabled': 'true',
                'SecurityGroupIds': [
                    {
                        'Fn::GetAtt': [
                            'VPCmonitoringSecurityGroup',
                            'GroupId'
                        ]
                    }
                ],
                'SubnetIds': [
                    {
                        'Ref': 'VPCPrivateSubnet1SubnetXYZ'
                    },
                    {
                        'Ref': 'VPCPrivateSubnet2SubnetABC'
                    }
                ],
                'VpcEndpointType': 'Interface'
            },
            '_key': 'VPCmonitoring'
        },
        'parent': '8f2c8747-641a-4a7e-8240-83e8e59d1ea7',
        'tags': [
            'AWS::EC2::VPCEndpoint'
        ],
        'id': 'cec47d5b-87ff-4a27-8146-53898c5a3c63',
        'parent_type': 'component'
    },
    {
        'name': 'Service',
        'type': 'elastic-container-service',
        'source': {
            'Type': 'AWS::ECS::Service',
            'Properties': {
                'NetworkConfiguration': {
                    'AwsvpcConfiguration': {
                        'AssignPublicIp': 'DISABLED',
                        'SecurityGroups': [
                            {
                                'Fn::GetAtt': [
                                    'OutboundSecurityGroup',
                                    'GroupId'
                                ]
                            }
                        ],
                        'Subnets': [
                            {
                                'Fn::ImportValue': 'ECSFargateGoVPCStack:ExportsOutputRefVPCPrivateSubnet1SubnetXYZ'
                            },
                            {
                                'Fn::ImportValue': 'ECSFargateGoVPCStack:ExportsOutputRefVPCPrivateSubnet2SubnetABC'
                            }
                        ]
                    }
                },
                'TaskDefinition': {
                    'Ref': 'ServiceTaskDefinition'
                }
            },
            '_key': 'Service'
        },
        'parent': '04fcb189-09f9-41d2-88f2-20c636b0adfc',
        'tags': [
            'AWS::ECS::Service'
        ],
        'id': '1120e381-0429-4a56-bfba-0513ba1f5585',
        'parent_type': 'component'
    },
    {
        'name': 'Service',
        'type': 'elastic-container-service',
        'source': {
            'Type': 'AWS::ECS::Service',
            'Properties': {
                'NetworkConfiguration': {
                    'AwsvpcConfiguration': {
                        'AssignPublicIp': 'DISABLED',
                        'SecurityGroups': [
                            {
                                'Fn::GetAtt': [
                                    'OutboundSecurityGroup',
                                    'GroupId'
                                ]
                            }
                        ],
                        'Subnets': [
                            {
                                'Fn::ImportValue': 'ECSFargateGoVPCStack:ExportsOutputRefVPCPrivateSubnet1SubnetXYZ'
                            },
                            {
                                'Fn::ImportValue': 'ECSFargateGoVPCStack:ExportsOutputRefVPCPrivateSubnet2SubnetABC'
                            }
                        ]
                    }
                },
                'TaskDefinition': {
                    'Ref': 'ServiceTaskDefinition'
                }
            },
            '_key': 'Service'
        },
        'parent': '8f2c8747-641a-4a7e-8240-83e8e59d1ea7',
        'tags': [
            'AWS::ECS::Service'
        ],
        'id': 'a54c938b-8e8c-4e27-90e8-7aae57090c25',
        'parent_type': 'component'
    },
    {
        'name': 'ServiceTaskDefinition',
        'type': 'docker-container',
        'source': {
            'Type': 'AWS::ECS::TaskDefinition',
            'Properties': {
                'ContainerDefinitions': [
                    {
                        'Environment': [
                            {
                                'Name': 'COUNTER_TABLE_NAME',
                                'Value': {
                                    'Fn::ImportValue': 'ECSFargateGoDataStack:ExportsOutputRefCounterTable0011223344556677'
                                }
                            }
                        ],
                        'Essential': 'true',
                        'Image': {
                            'Fn::Sub': '${AWS::AccountId}.dkr.ecr.us-east-1.${AWS::URLSuffix}/cdk-aa001122ds-container-assets-${AWS::AccountId}-us-east-1:00112233445566778899'
                        },
                        'LogConfiguration': {
                            'LogDriver': 'awslogs',
                            'Options': {
                                'awslogs-group': {
                                    'Ref': 'CounterServiceTaskDefwebLogGroupAABBCCDD'
                                },
                                'awslogs-stream-prefix': 'CounterService',
                                'awslogs-region': 'us-east-1'
                            }
                        },
                        'Name': 'web',
                        'PortMappings': [
                            {
                                'ContainerPort': '80',
                                'Protocol': 'tcp'
                            }
                        ]
                    }
                ],
                'Cpu': '256',
                'ExecutionRoleArn': {
                    'Fn::GetAtt': [
                        'CounterServiceTaskDefExecutionRoleBBDDEEFF',
                        'Arn'
                    ]
                },
                'Family': 'ECSFargateGoServiceStackCounterServiceTaskDefAABBCCDD',
                'Memory': '512',
                'NetworkMode': 'awsvpc',
                'RequiresCompatibilities': [
                    'FARGATE'
                ],
                'TaskRoleArn': {
                    'Fn::GetAtt': [
                        'ECSTaskRoleF2ADB362',
                        'Arn'
                    ]
                }
            },
            'UpdateReplacePolicy': 'Delete',
            'DeletionPolicy': 'Delete',
            'Metadata': {
                'aws:cdk:path': 'ECSFargateGoServiceStack/CounterService/TaskDef/Resource'
            },
            '_key': 'ServiceTaskDefinition'
        },
        'parent': '1120e381-0429-4a56-bfba-0513ba1f5585',
        'tags': [
            'AWS::ECS::TaskDefinition'
        ],
        'id': '3992e9e8-cecb-4894-9e12-c4fa235ac531',
        'parent_type': 'component'
    },
    {
        'name': 'ServiceTaskDefinition',
        'type': 'docker-container',
        'source': {
            'Type': 'AWS::ECS::TaskDefinition',
            'Properties': {
                'ContainerDefinitions': [
                    {
                        'Environment': [
                            {
                                'Name': 'COUNTER_TABLE_NAME',
                                'Value': {
                                    'Fn::ImportValue': 'ECSFargateGoDataStack:ExportsOutputRefCounterTable0011223344556677'
                                }
                            }
                        ],
                        'Essential': 'true',
                        'Image': {
                            'Fn::Sub': '${AWS::AccountId}.dkr.ecr.us-east-1.${AWS::URLSuffix}/cdk-aa001122ds-container-assets-${AWS::AccountId}-us-east-1:00112233445566778899'
                        },
                        'LogConfiguration': {
                            'LogDriver': 'awslogs',
                            'Options': {
                                'awslogs-group': {
                                    'Ref': 'CounterServiceTaskDefwebLogGroupAABBCCDD'
                                },
                                'awslogs-stream-prefix': 'CounterService',
                                'awslogs-region': 'us-east-1'
                            }
                        },
                        'Name': 'web',
                        'PortMappings': [
                            {
                                'ContainerPort': '80',
                                'Protocol': 'tcp'
                            }
                        ]
                    }
                ],
                'Cpu': '256',
                'ExecutionRoleArn': {
                    'Fn::GetAtt': [
                        'CounterServiceTaskDefExecutionRoleBBDDEEFF',
                        'Arn'
                    ]
                },
                'Family': 'ECSFargateGoServiceStackCounterServiceTaskDefAABBCCDD',
                'Memory': '512',
                'NetworkMode': 'awsvpc',
                'RequiresCompatibilities': [
                    'FARGATE'
                ],
                'TaskRoleArn': {
                    'Fn::GetAtt': [
                        'ECSTaskRoleF2ADB362',
                        'Arn'
                    ]
                }
            },
            'UpdateReplacePolicy': 'Delete',
            'DeletionPolicy': 'Delete',
            'Metadata': {
                'aws:cdk:path': 'ECSFargateGoServiceStack/CounterService/TaskDef/Resource'
            },
            '_key': 'ServiceTaskDefinition'
        },
        'parent': 'a54c938b-8e8c-4e27-90e8-7aae57090c25',
        'tags': [
            'AWS::ECS::TaskDefinition'
        ],
        'id': '07c34f7e-ee28-4c3b-9a20-2f0c4875520c',
        'parent_type': 'component'
    },
    {
        'name': 'ServiceLB',
        'type': 'load-balancer',
        'source': {
            'Type': 'AWS::ElasticLoadBalancingV2::LoadBalancer',
            'Properties': {
                'LoadBalancerAttributes': [
                    {
                        'Key': 'deletion_protection.enabled',
                        'Value': 'false'
                    }
                ],
                'Scheme': 'internal',
                'SecurityGroups': [
                    {
                        'Fn::GetAtt': [
                            'ServiceLBSecurityGroup',
                            'GroupId'
                        ]
                    }
                ],
                'Subnets': [
                    {
                        'Fn::ImportValue': 'ECSFargateGoVPCStack:ExportsOutputRefVPCPrivateSubnet1SubnetXYZ'
                    },
                    {
                        'Fn::ImportValue': 'ECSFargateGoVPCStack:ExportsOutputRefVPCPrivateSubnet2SubnetABC'
                    }
                ],
                'Type': 'application'
            },
            '_key': 'ServiceLB'
        },
        'parent': '04fcb189-09f9-41d2-88f2-20c636b0adfc',
        'tags': [
            'AWS::ElasticLoadBalancingV2::LoadBalancer'
        ],
        'id': 'd7aad912-6382-4f68-a411-2318d5d1325a',
        'parent_type': 'component'
    },
    {
        'name': 'ServiceLB',
        'type': 'load-balancer',
        'source': {
            'Type': 'AWS::ElasticLoadBalancingV2::LoadBalancer',
            'Properties': {
                'LoadBalancerAttributes': [
                    {
                        'Key': 'deletion_protection.enabled',
                        'Value': 'false'
                    }
                ],
                'Scheme': 'internal',
                'SecurityGroups': [
                    {
                        'Fn::GetAtt': [
                            'ServiceLBSecurityGroup',
                            'GroupId'
                        ]
                    }
                ],
                'Subnets': [
                    {
                        'Fn::ImportValue': 'ECSFargateGoVPCStack:ExportsOutputRefVPCPrivateSubnet1SubnetXYZ'
                    },
                    {
                        'Fn::ImportValue': 'ECSFargateGoVPCStack:ExportsOutputRefVPCPrivateSubnet2SubnetABC'
                    }
                ],
                'Type': 'application'
            },
            '_key': 'ServiceLB'
        },
        'parent': '8f2c8747-641a-4a7e-8240-83e8e59d1ea7',
        'tags': [
            'AWS::ElasticLoadBalancingV2::LoadBalancer'
        ],
        'id': '190e97cd-3c65-4c49-a420-bf142d323e3d',
        'parent_type': 'component'
    },
    {
        'name': 'Canary',
        'type': 'empty-component',
        'source': {
            'Type': 'AWS::Synthetics::Canary',
            'Properties': {
                'VPCConfig': {
                    'SecurityGroupIds': [
                        {
                            'Fn::GetAtt': [
                                'CanarySecurityGroup',
                                'GroupId'
                            ]
                        }
                    ],
                    'SubnetIds': [
                        {
                            'Fn::ImportValue': 'ECSFargateGoVPCStack:ExportsOutputRefVPCPublicSubnet1SubnetHIJ'
                        },
                        {
                            'Fn::ImportValue': 'ECSFargateGoVPCStack:ExportsOutputRefVPCPublicSubnet2SubnetKLM'
                        }
                    ]
                }
            },
            '_key': 'Canary'
        },
        'parent': 'b4085343-2934-4c4d-8148-67c1bf4cc070',
        'tags': [
            'AWS::Synthetics::Canary'
        ],
        'id': 'e82dbb96-3a7e-46c9-afae-f259336a8379',
        'parent_type': 'component'
    },
    {
        'name': 'Canary',
        'type': 'empty-component',
        'source': {
            'Type': 'AWS::Synthetics::Canary',
            'Properties': {
                'VPCConfig': {
                    'SecurityGroupIds': [
                        {
                            'Fn::GetAtt': [
                                'CanarySecurityGroup',
                                'GroupId'
                            ]
                        }
                    ],
                    'SubnetIds': [
                        {
                            'Fn::ImportValue': 'ECSFargateGoVPCStack:ExportsOutputRefVPCPublicSubnet1SubnetHIJ'
                        },
                        {
                            'Fn::ImportValue': 'ECSFargateGoVPCStack:ExportsOutputRefVPCPublicSubnet2SubnetKLM'
                        }
                    ]
                }
            },
            '_key': 'Canary'
        },
        'parent': 'f1d093a9-b0e7-4548-8e2f-b6d0f4a3fa26',
        'tags': [
            'AWS::Synthetics::Canary'
        ],
        'id': '7df85b9d-1e35-4551-a157-b91fe032a182',
        'parent_type': 'component'
    },
    {
        'name': '0.0.0.0/0',
        'type': 'generic-client',
        'source': {
            'Type': 'AWS::EC2::SecurityGroup',
            'Properties': {
                'GroupDescription': 'ECSFargateGoVPCStack/VPC/ssm/SecurityGroup',
                'SecurityGroupEgress': [
                    {
                        'CidrIp': '0.0.0.0/0',
                        'Description': 'Allow all outbound traffic by default',
                        'IpProtocol': '-1'
                    }
                ],
                'SecurityGroupIngress': [
                    {
                        'CidrIp': {
                            'Fn::GetAtt': [
                                'CustomVPC',
                                'CidrBlock'
                            ]
                        },
                        'Description': {
                            'Fn::Join': [
                                '',
                                [
                                    'from ',
                                    {
                                        'Fn::GetAtt': [
                                            'CustomVPC',
                                            'CidrBlock'
                                        ]
                                    },
                                    ':443'
                                ]
                            ]
                        },
                        'FromPort': '443',
                        'IpProtocol': 'tcp',
                        'ToPort': '443'
                    }
                ],
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'ECSFargateGoVPCStack/VPC'
                    }
                ],
                'VpcId': {
                    'Ref': 'CustomVPC'
                }
            },
            '_key': 'VPCssmSecurityGroup'
        },
        'parent': 'f0ba7722-39b6-4c81-8290-a30a248bb8d9',
        'tags': [
            'Outbound connection destination IP'
        ],
        'id': '11dd4b56-7033-4a94-875a-4180a0164865',
        'parent_type': 'trustZone'
    },
    {
        'name': '255.255.255.255/32',
        'type': 'generic-client',
        'source': {
            'Type': 'AWS::EC2::SecurityGroup',
            'Properties': {
                'GroupDescription': 'ECSFargateGoServiceStack/OutboundSecurityGroup',
                'SecurityGroupEgress': [
                    {
                        'CidrIp': '255.255.255.255/32',
                        'Description': 'Disallow all traffic',
                        'FromPort': '252',
                        'IpProtocol': 'icmp',
                        'ToPort': '86'
                    }
                ],
                'VpcId': {
                    'Fn::ImportValue': 'ECSFargateGoVPCStack:ExportsOutputRefCustomVPCBDGHIJK'
                }
            },
            '_key': 'OutboundSecurityGroup'
        },
        'parent': 'f0ba7722-39b6-4c81-8290-a30a248bb8d9',
        'tags': [
            'Outbound connection destination IP'
        ],
        'id': 'a0985c4f-4ce3-4cf5-8ac2-5da8027fc2c2',
        'parent_type': 'trustZone'
    },
    {
        'name': 'CustomVPC',
        'type': 'vpc',
        'source': {
            'Type': 'AWS::EC2::VPC',
            'Properties': {
                'CidrBlock': '10.0.0.0/16'
            },
            '_key': 'CustomVPC'
        },
        'parent': 'b61d6911-338d-46a8-9f39-8dcd24abfe91',
        'tags': [
            'AWS::EC2::VPC'
        ],
        'id': '31401380-c6c5-41ad-a0d1-65d6ff93ebd9',
        'parent_type': 'trustZone'
    }
])


class TestCloudformationPathIdsCalculator:

    def test_calculate_path_ids(self):
        # GIVEN a list of hierarchical components
        components = SGS_COMPONENTS

        # WHEN calling calculate_path_ids
        path_ids = CloudformationPathIdsCalculator(components).calculate_path_ids()

        # THEN there are 22 resultant components
        assert len(components) == 21

        # AND Each ID match its whole path
        assert path_ids[
                   '31401380-c6c5-41ad-a0d1-65d6ff93ebd9'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc'
        assert path_ids[
                   '04fcb189-09f9-41d2-88f2-20c636b0adfc'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1'
        assert path_ids[
                   '8f2c8747-641a-4a7e-8240-83e8e59d1ea7'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2'
        assert path_ids[
                   'b4085343-2934-4c4d-8148-67c1bf4cc070'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.publicsubnet1'
        assert path_ids[
                   'f1d093a9-b0e7-4548-8e2f-b6d0f4a3fa26'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.publicsubnet2'
        assert path_ids[
                   '18c59d7c-acb7-4210-b060-4074a0ab012e'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.vpcssm-altsource'
        assert path_ids[
                   'eed89218-8388-412f-b357-b4240c0e57fe'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.vpcssm-altsource'
        assert path_ids[
                   'ee00a4cf-39c2-4459-8c72-345d89320634'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.vpcssmmessages-altsource'
        assert path_ids[
                   '41aaf28a-2b7e-4c73-b6e7-c347f2006fdd'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.vpcssmmessages-altsource'
        assert path_ids[
                   'bda1120b-1e0e-430a-97f2-480d8953a3d7'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.vpcmonitoring'
        assert path_ids[
                   'cec47d5b-87ff-4a27-8146-53898c5a3c63'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.vpcmonitoring'
        assert path_ids[
                   '1120e381-0429-4a56-bfba-0513ba1f5585'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.service'
        assert path_ids[
                   'a54c938b-8e8c-4e27-90e8-7aae57090c25'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.service'
        assert path_ids[
                   '3992e9e8-cecb-4894-9e12-c4fa235ac531'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.service.servicetaskdefinition'
        assert path_ids[
                   '07c34f7e-ee28-4c3b-9a20-2f0c4875520c'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.service.servicetaskdefinition'
        assert path_ids[
                   'd7aad912-6382-4f68-a411-2318d5d1325a'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet1.servicelb'
        assert path_ids[
                   '190e97cd-3c65-4c49-a420-bf142d323e3d'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.privatesubnet2.servicelb'
        assert path_ids[
                   'e82dbb96-3a7e-46c9-afae-f259336a8379'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.publicsubnet1.canary'
        assert path_ids[
                   '7df85b9d-1e35-4551-a157-b91fe032a182'] == 'b61d6911-338d-46a8-9f39-8dcd24abfe91.customvpc.publicsubnet2.canary'
        assert path_ids[
                   '11dd4b56-7033-4a94-875a-4180a0164865'] == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9.vpcssmsecuritygroup.0_0_0_0_0'
        assert path_ids[
                   'a0985c4f-4ce3-4cf5-8ac2-5da8027fc2c2'] == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9.outboundsecuritygroup.255_255_255_255_32'
