from pytest import mark

from slp_tf.slp_tf.parse.mapping.search.functions.tf_query_mapping_functions import query


class TestTfQueryMappingFunctions:
    source_model_data = {
        "resource": [
            {
                "aws_vpc_endpoint": {},
                "resource_type": "aws_vpc_endpoint",
                "resource_name": "VPCssm",
                "resource_properties": {
                    "vpc_id": "${aws_vpc.CustomVPC.id}",
                    "service_name": "the.service.name",
                    "vpc_endpoint_type": "Interface",
                    "security_group_ids": [
                        "${aws_security_group.VPCssmSecurityGroup.id}"
                    ],
                    "subnet_ids": [
                        "${aws_subnet.PrivateSubnet1.id}",
                        "${aws_subnet.PrivateSubnet2.id}"
                    ],
                    "private_dns_enabled": True
                }
            },
            {
                "aws_vpc": {},
                "resource_type": "aws_vpc",
                "resource_name": "vpc",
                "resource_properties": {
                    "cidr_block": "var.vpcCidrblock"
                }
            }
        ]
    }

    source_model_data_redos = {
        "resource": [
            {
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa2": {},
                "resource_type": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa2",
                "resource_name": "redos_component1",
                "resource_properties": {
                    "cidr_block": "var.vpcCidrblock"
                }
            },
            {
                "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa": {},
                "resource_type": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "resource_name": "redos_component2",
                "resource_properties": {
                    "cidr_block": "var.vpcCidrblock"
                }
            }
        ]
    }

    def test_query_with_type(self):
        mapping_source = {"$type": "aws_vpc_endpoint"}
        data = query(mapping_source, source_model_data=self.source_model_data)
        assert len(data) == 1
        assert data[0]['resource_type'] == 'aws_vpc_endpoint'

    def test_query_with_type_list(self):
        mapping_source = {"$type": ["aws_vpc_endpoint", "aws_vpc"]}
        data = query(mapping_source, source_model_data=self.source_model_data)
        assert len(data) == 2
        assert data[0]['resource_type'] == 'aws_vpc_endpoint'
        assert data[1]['resource_type'] == 'aws_vpc'

    def test_query_with_name(self):
        mapping_source = {"$name": "VPCssm"}
        data = query(mapping_source, source_model_data=self.source_model_data)
        assert len(data) == 1
        assert data[0]['resource_type'] == 'aws_vpc_endpoint'

    def test_query_with_name_list(self):
        mapping_source = {"$name": ["VPCssm", "vpc"]}
        data = query(mapping_source, source_model_data=self.source_model_data)
        assert len(data) == 2
        assert data[0]['resource_type'] == 'aws_vpc_endpoint'
        assert data[1]['resource_type'] == 'aws_vpc'

    def test_query_with_props(self):
        mapping_source = {"$props": "vpc_id"}
        data = query(mapping_source, source_model_data=self.source_model_data)
        assert len(data) == 1
        assert data[0]['resource_type'] == 'aws_vpc_endpoint'

    def test_query_with_props_list(self):
        mapping_source = {"$props": ["vpc_id", "cidr_block"]}
        data = query(mapping_source, source_model_data=self.source_model_data)
        assert len(data) == 2
        assert data[0]['resource_type'] == 'aws_vpc_endpoint'
        assert data[1]['resource_type'] == 'aws_vpc'

    def test_query_with_type_regex(self):
        mapping_source = {"$type": {"$regex": "^aws_vpc_\\w*$"}}
        data = query(mapping_source, source_model_data=self.source_model_data)
        assert len(data) == 1
        assert data[0]['resource_type'] == 'aws_vpc_endpoint'


    @mark.parametrize('regex', [ "^a+$", "^(a+)+$"])
    def test_query_with_type_regex_long_name(self,regex):
        mapping_source = {"$type": {"$regex": regex}}
        data = query(mapping_source, source_model_data=self.source_model_data_redos)
        assert len(data) == 1
        assert data[0]['resource_type'] == 'a' * 59

