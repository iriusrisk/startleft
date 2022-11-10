from unittest.mock import patch, MagicMock

from slp_cft.slp_cft.parse.mapping.mappers.cft_base_mapper import CloudformationBaseMapper
from slp_cft.slp_cft.parse.mapping.cft_sourcemodel import CloudformationSourceModel
from slp_cft.slp_cft.load.cft_loader import CloudformationLoader
from sl_util.sl_util.file_utils import get_data
from slp_cft.tests.resources import test_resource_paths

REF_FUNCTION_COMMON_SOURCE = {'Type': 'AWS::EC2::SecurityGroup', 'Condition': 'EC2SecurityEnabled', 'Properties':
            {'VpcId': {'Ref': 'SimpleVPC'}, 'GroupName': {'Fn::Join': ['-', [{'Ref': 'NamingPrefix'}, 'SG']]},
             'GroupDescription': 'Enable HTTP access via port 80 and 443 to the allowed CIDR',
             'SecurityGroupEgress': [{'IpProtocol': 'tcp', 'FromPort': '80', 'ToPort': '80',
                                      'CidrIp': {'Ref': 'PublicSGSource'}}, {'IpProtocol': 'tcp', 'FromPort': '443',
                                                                             'ToPort': '443', 'CidrIp':
                                                                                 {'Ref': 'PublicSGSource'}}],
             'Tags': [{'Key': 'Name', 'Value': {'Fn::Join': ['-', [{'Ref': 'NamingPrefix'},
                                                                   'SG']]}}]}, '_key': 'PublicSecurityGroup'}


class TestCloudformationBaseMapper:

    @patch("slp_cft.slp_cft.parse.mapping.cft_sourcemodel.CloudformationSourceModel")
    def test_get_tags_with_mapping_str(self, mock_source_model):
        mock_source_model.search.return_value = 'value'
        c_tags = CloudformationBaseMapper.get_tags(mock_source_model, MagicMock(), MagicMock())
        assert len(c_tags) is 1

    @patch("slp_cft.slp_cft.parse.mapping.cft_sourcemodel.CloudformationSourceModel")
    def test_get_tags_with_mapping_list(self, mock_source_model):
        mock_source_model.search.return_value = 'value'
        c_tags = CloudformationBaseMapper.get_tags(mock_source_model, MagicMock(), [MagicMock(), MagicMock()])
        assert len(c_tags) is 2

    @patch("slp_cft.slp_cft.parse.mapping.cft_sourcemodel.CloudformationSourceModel")
    def test_get_tags_with_attribute_not_found(self, mock_source_model):
        mock_source_model.search.return_value = []
        c_tags = CloudformationBaseMapper.get_tags(mock_source_model, MagicMock(), MagicMock())
        assert len(c_tags) is 0

    def test_retrieve_name_with_ref_function_parameters_and_default(self):
        # GIVEN a cloudformation JSON file
        # AND the ref value is a Parameter with Default Attribute
        cft_file = get_data(test_resource_paths.cloudformation_with_ref_function_and_default_property_json)
        cft_loader = CloudformationLoader([cft_file])
        cft_loader.load()

        # AND a mapping path that matches a component whose name is a Ref Value
        obj = 'Properties.SecurityGroupEgress[0].CidrIp'
        cft_source_model = CloudformationSourceModel(cft_loader.cloudformation)

        # WHEN parsing the file
        result = cft_source_model._CloudformationSourceModel__jmespath_search(obj, REF_FUNCTION_COMMON_SOURCE)

        # THEN the component name is the Default attribute of the parameter
        assert result == '0.0.0.0/0'

    def test_retrieve_name_with_ref_function_parameters_without_default(self):
        # GIVEN a cloudformation JSON file
        # AND the ref value is a Parameter without Default Attribute
        cft_file = get_data(test_resource_paths.cloudformation_with_ref_function_and_without_default_property_json)
        cft_loader = CloudformationLoader([cft_file])
        cft_loader.load()

        # AND a mapping path that matches a component whose name is a Ref Value
        obj = 'Properties.SecurityGroupEgress[0].CidrIp'
        cft_source_model = CloudformationSourceModel(cft_loader.cloudformation)

        # WHEN parsing the file
        result = cft_source_model._CloudformationSourceModel__jmespath_search(obj, REF_FUNCTION_COMMON_SOURCE)

        # THEN the component name is the name of the Parameter
        assert result == 'PublicSGSource'

    def test_retrieve_name_with_ref_function_without_parameters(self):
        # GIVEN a cloudformation JSON file
        # AND the ref value is a Parameter without Parameters
        cft_file = get_data(test_resource_paths.cloudformation_with_ref_function_and_without_parameters)
        cft_loader = CloudformationLoader([cft_file])
        cft_loader.load()

        # AND a mapping path that matches a component whose name is a Ref Value
        obj = 'Properties.SecurityGroupEgress[0].CidrIp'
        cft_source_model = CloudformationSourceModel(cft_loader.cloudformation)

        # WHEN parsing the file
        result = cft_source_model._CloudformationSourceModel__jmespath_search(obj, REF_FUNCTION_COMMON_SOURCE)

        # THEN the component name is the name of the Parameter
        assert result == 'PublicSGSource'
