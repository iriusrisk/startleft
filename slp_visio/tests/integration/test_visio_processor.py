from pytest import mark

from sl_util.sl_util.file_utils import get_data
from slp_base.tests.util.otm import validate_and_diff
from slp_base.tests.util.otm import check_otm_representations_size, check_otm_trustzone, public_cloud_id, \
    public_cloud_name, check_otm_component, check_otm_dataflow, public_cloud_type, private_secured_type, internet_type
from slp_visio.slp_visio.visio_processor import VisioProcessor
from slp_visio.tests.resources import test_resource_paths
from slp_visio.tests.resources.test_resource_paths import expected_empty_mapping_file, expected_empty_visio_file, \
    expected_empty_mapping_and_visio_files, expected_aws_shapes, expected_generic_elements, \
    expected_self_pointing_connectors, expected_extraneous_elements, expected_simple_boundary_tzs, \
    expected_boundary_tz_and_default_tz, expected_overlapped_boundary_tzs, \
    expected_visio_boundary_and_component_tzs, expected_multiple_pages_diagram, expected_complex_diagram, \
    expected_prune_orphan_connectors, expected_bidirectional_connectors, expected_manually_modified_connectors

VALIDATION_EXCLUDED_REGEX = r"root\[\'dataflows'\]\[.+?\]\['name'\]"


class TestVisioProcessor:

    @mark.parametrize('vsdx,mapping', [
        (test_resource_paths.visio_aws_shapes, test_resource_paths.empty_mapping),
        (test_resource_paths.visio_empty, test_resource_paths.default_visio_mapping),
        (test_resource_paths.visio_empty, test_resource_paths.default_visio_mapping_legacy),
        (test_resource_paths.visio_empty, test_resource_paths.empty_mapping)
    ])
    def test_empties(self, vsdx, mapping):
        visio_file = open(vsdx, "r")
        otm = VisioProcessor("project-id", "project-name", visio_file, [get_data(mapping)]).process()

        assert len(otm.trustzones) == 0
        assert len(otm.components) == 0
        assert len(otm.dataflows) == 0

    @mark.parametrize('mapping', [
        test_resource_paths.default_visio_mapping,
        test_resource_paths.default_visio_mapping_legacy,
    ])
    def test_aws_shapes(self, mapping):
        visio_file = open(test_resource_paths.visio_aws_shapes, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(mapping)],
        ).process()

        assert len(otm.trustzones) == 1
        assert len(otm.components) == 5
        assert len(otm.dataflows) == 4

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_type, public_cloud_name)

        check_otm_component(otm, 0, 'ec2', 'Amazon EC2')
        check_otm_component(otm, 1, 'ec2', 'Custom machine')
        check_otm_component(otm, 2, 'rds', 'Private Database')
        check_otm_component(otm, 3, 'cloudwatch', 'Amazon CloudWatch')
        check_otm_component(otm, 4, 'cloudwatch', 'Custom log system')

        check_otm_dataflow(otm, 0, '1', '12')
        check_otm_dataflow(otm, 1, '12', '30')
        check_otm_dataflow(otm, 2, '1', '35')
        check_otm_dataflow(otm, 3, '12', '41')

    @mark.parametrize('mapping', [
        test_resource_paths.custom_vpc_mapping,
        test_resource_paths.custom_vpc_mapping_legacy,
    ])
    def test_generic_elements(self, mapping):
        visio_file = open(test_resource_paths.visio_generic_shapes, "r")
        otm = VisioProcessor("project-id", "project-name", visio_file, [get_data(mapping)]).process()

        assert len(otm.trustzones) == 1
        assert len(otm.components) == 2
        assert len(otm.dataflows) == 1

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_type, public_cloud_name)

        check_otm_component(otm, 0, 'empty-component', 'Custom enterprise GW')
        check_otm_component(otm, 1, 'empty-component', 'Custom web server')

    @mark.parametrize('mapping', [
        test_resource_paths.custom_vpc_mapping,
        test_resource_paths.custom_vpc_mapping_legacy,
    ])
    def test_self_pointing_connectors(self, mapping):
        visio_file = open(test_resource_paths.visio_self_pointing_connectors, "r")
        otm = VisioProcessor("project-id", "project-name", visio_file, [get_data(mapping)]).process()

        assert len(otm.trustzones) == 1
        assert len(otm.components) == 2
        assert len(otm.dataflows) == 0

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_type, public_cloud_name)

        check_otm_component(otm, 0, 'empty-component', 'Custom enterprise GW')
        check_otm_component(otm, 1, 'empty-component', 'Custom web server')

    @mark.parametrize('mapping', [
        test_resource_paths.default_visio_mapping,
        test_resource_paths.default_visio_mapping_legacy,
    ])
    def test_extraneous_elements(self, mapping):
        visio_file = open(test_resource_paths.visio_extraneous_elements, "r")
        otm = VisioProcessor("project-id", "project-name", visio_file, [get_data(mapping)]).process()

        assert len(otm.trustzones) == 2
        assert len(otm.components) == 5
        assert len(otm.dataflows) == 4

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, '47', public_cloud_type, 'Public Cloud')
        check_otm_trustzone(otm, 1, '48', private_secured_type, 'Private Secured Cloud')

        check_otm_component(otm, 0, 'ec2', 'Amazon EC2')
        check_otm_component(otm, 1, 'ec2', 'Custom machine')
        check_otm_component(otm, 2, 'rds', 'Private Database')
        check_otm_component(otm, 3, 'cloudwatch', 'Amazon CloudWatch')
        check_otm_component(otm, 4, 'cloudwatch', 'Custom log system')

        check_otm_dataflow(otm, 0, '1', '12')
        check_otm_dataflow(otm, 1, '12', '30')
        check_otm_dataflow(otm, 2, '1', '35')
        check_otm_dataflow(otm, 3, '12', '41')

    @mark.parametrize('mapping', [
        test_resource_paths.default_visio_mapping,
        test_resource_paths.default_visio_mapping_legacy,
    ])
    def test_simple_boundary_tzs(self, mapping):
        visio_file = open(test_resource_paths.visio_simple_boundary_tzs, "r")
        otm = VisioProcessor("project-id", "project-name", visio_file, [get_data(mapping)]).process()

        assert len(otm.trustzones) == 2
        assert len(otm.components) == 2
        assert len(otm.dataflows) == 1

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, '62', public_cloud_type, 'Public Cloud')
        check_otm_trustzone(otm, 1, '64', private_secured_type, 'Private Secured Cloud')

        check_otm_component(otm, 0, 'ec2', 'Custom machine', '62')
        check_otm_component(otm, 1, 'rds', 'Private Database', '64')

        check_otm_dataflow(otm, 0, '12', '30')

    @mark.parametrize('mapping', [
        test_resource_paths.default_visio_mapping,
        test_resource_paths.default_visio_mapping_legacy,
    ])
    def test_boundary_tz_and_default_tz(self, mapping):
        visio_file = open(test_resource_paths.visio_boundary_tz_and_default_tz, "r")
        otm = VisioProcessor("project-id", "project-name", visio_file, [get_data(mapping)]).process()

        assert len(otm.trustzones) == 2
        assert len(otm.components) == 2
        assert len(otm.dataflows) == 1

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, '64', private_secured_type, 'Private Secured Cloud')
        check_otm_trustzone(otm, 1, '804b664a-7129-4a9e-a08c-16a99669f605', public_cloud_type, 'Public Cloud')

        check_otm_component(otm, 0, 'ec2', 'Custom machine', '804b664a-7129-4a9e-a08c-16a99669f605')
        check_otm_component(otm, 1, 'rds', 'Private Database', '64')

        check_otm_dataflow(otm, 0, '12', '30')

    @mark.parametrize('mapping', [
        test_resource_paths.default_visio_mapping,
        test_resource_paths.default_visio_mapping_legacy,
    ])
    def test_overlapped_boundary_tzs(self, mapping):
        visio_file = open(test_resource_paths.visio_overlapped_boundary_tzs, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(mapping)],
        ).process()

        assert len(otm.trustzones) == 2
        assert len(otm.components) == 2
        assert len(otm.dataflows) == 1

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, '62', public_cloud_type, 'Public Cloud')
        check_otm_trustzone(otm, 1, '64', private_secured_type, 'Private Secured Cloud')

        check_otm_component(otm, 0, 'ec2', 'Custom machine', '62')
        check_otm_component(otm, 1, 'rds', 'Private Database', '64')

        check_otm_dataflow(otm, 0, '12', '30')

    @mark.parametrize('mapping', [
        test_resource_paths.default_visio_mapping,
        test_resource_paths.default_visio_mapping_legacy,
    ])
    def test_visio_boundary_and_component_tzs(self, mapping):
        visio_file = open(test_resource_paths.visio_boundary_and_component_tzs, "r")
        otm = VisioProcessor("project-id", "project-name", visio_file, [get_data(mapping)]).process()

        assert len(otm.trustzones) == 2
        assert len(otm.components) == 2
        assert len(otm.dataflows) == 1

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, '66', internet_type, 'Internet')
        check_otm_trustzone(otm, 1, '64', private_secured_type, 'Private Secured Cloud')

        check_otm_component(otm, 0, 'ec2', 'Custom machine', '66')
        check_otm_component(otm, 1, 'rds', 'Private Database', '64')

        check_otm_dataflow(otm, 0, '12', '30')

    @mark.parametrize('mapping', [
        test_resource_paths.default_visio_mapping,
        test_resource_paths.default_visio_mapping_legacy,
    ])
    def test_multiple_pages_diagram(self, mapping):
        visio_file = open(test_resource_paths.visio_multiple_pages_diagram, "r")
        otm = VisioProcessor("project-id", "project-name", visio_file, [get_data(mapping)]).process()

        assert len(otm.trustzones) == 3
        assert len(otm.components) == 3
        assert len(otm.dataflows) == 2

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, '62', public_cloud_type, 'Public Cloud')
        check_otm_trustzone(otm, 1, '64', private_secured_type, 'Private Secured Cloud')
        check_otm_trustzone(otm, 2, '70', internet_type, 'Internet')

        check_otm_component(otm, 0, 'ec2', 'Custom machine', '62')
        check_otm_component(otm, 1, 'rds', 'Private Database', '64')
        check_otm_component(otm, 2, 'ec2', 'Internet Machine', '70')

        check_otm_dataflow(otm, 0, '12', '30')
        check_otm_dataflow(otm, 1, '65', '30')

    @mark.parametrize('mapping', [
        test_resource_paths.default_visio_mapping,
        test_resource_paths.default_visio_mapping_legacy,
    ])
    def test_complex_diagram(self, mapping):
        visio_file = open(test_resource_paths.visio_aws_with_tz_and_vpc, "r")
        otm = VisioProcessor("project-id", "project-name", visio_file, [get_data(mapping)]).process()

        assert len(otm.trustzones) == 2
        assert len(otm.components) == 5
        assert len(otm.dataflows) == 4

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, '47', public_cloud_type, 'Public Cloud')
        check_otm_trustzone(otm, 1, '48', private_secured_type, 'Private Secured Cloud')

        check_otm_component(otm, 0, 'ec2', 'Amazon EC2')
        check_otm_component(otm, 1, 'ec2', 'Custom machine')
        check_otm_component(otm, 2, 'rds', 'Private Database')
        check_otm_component(otm, 3, 'cloudwatch', 'Amazon CloudWatch')
        check_otm_component(otm, 4, 'cloudwatch', 'Custom log system')

        check_otm_dataflow(otm, 0, '1', '12')
        check_otm_dataflow(otm, 1, '12', '30')
        check_otm_dataflow(otm, 2, '1', '35')
        check_otm_dataflow(otm, 3, '12', '41')

    @mark.parametrize('mapping', [
        test_resource_paths.default_visio_mapping,
        test_resource_paths.default_visio_mapping_legacy,
    ])
    def test_prune_orphan_connectors(self, mapping):
        visio_file = open(test_resource_paths.visio_orphan_dataflows, "r")
        otm = VisioProcessor("project-id", "project-name", visio_file, [get_data(mapping)]).process()

        assert len(otm.trustzones) == 1
        assert len(otm.components) == 6
        assert len(otm.dataflows) == 5

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_type, public_cloud_name)

        check_otm_component(otm, 0, 's3', 'Bucket')
        check_otm_component(otm, 1, 's3', 'Bucket')
        check_otm_component(otm, 2, 'CD-MQ', 'Amazon MQ')
        check_otm_component(otm, 3, 'CD-MQ', 'Amazon MQ')
        check_otm_component(otm, 4, 'rds', 'Database')
        check_otm_component(otm, 5, 'CD-MQ', 'Amazon MQ')

        check_otm_dataflow(otm, 0, '31', '19')
        check_otm_dataflow(otm, 1, '46', '19')
        check_otm_dataflow(otm, 2, '99', '19')
        check_otm_dataflow(otm, 3, '99', '86')
        check_otm_dataflow(otm, 4, '46', '13')

    @mark.parametrize('mapping', [
        test_resource_paths.default_visio_mapping,
        test_resource_paths.default_visio_mapping_legacy,
    ])
    def test_bidirectional_connectors(self, mapping):
        visio_file = open(test_resource_paths.visio_bidirectional_connectors, "r")
        otm = VisioProcessor("project-id", "project-name", visio_file, [get_data(mapping)]).process()

        assert len(otm.trustzones) == 1
        assert len(otm.components) == 6
        assert len(otm.dataflows) == 3

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, '804b664a-7129-4a9e-a08c-16a99669f605', public_cloud_type, 'Public Cloud')

        check_otm_component(otm, 0, 'ec2', 'Amazon EC2', '804b664a-7129-4a9e-a08c-16a99669f605')
        check_otm_component(otm, 1, 'ec2', 'Amazon EC2', '804b664a-7129-4a9e-a08c-16a99669f605')
        check_otm_component(otm, 2, 'ec2', 'Amazon EC2', '804b664a-7129-4a9e-a08c-16a99669f605')
        check_otm_component(otm, 3, 'vpc', 'Amazon VPC', '804b664a-7129-4a9e-a08c-16a99669f605')
        check_otm_component(otm, 4, 'vpc', 'Amazon VPC', '804b664a-7129-4a9e-a08c-16a99669f605')
        check_otm_component(otm, 5, 'vpc', 'Amazon VPC', '804b664a-7129-4a9e-a08c-16a99669f605')

        check_otm_dataflow(otm, 0, '23', '1', True)
        check_otm_dataflow(otm, 1, '28', '6', True)
        check_otm_dataflow(otm, 2, '33', '17', True)

    @mark.parametrize('mapping', [
        test_resource_paths.default_visio_mapping,
        test_resource_paths.default_visio_mapping_legacy,
    ])
    def test_manually_modified_connectors(self, mapping):
        visio_file = open(test_resource_paths.visio_modified_single_connectors, "r")
        otm = VisioProcessor("project-id", "project-name", visio_file, [get_data(mapping)]).process()

        assert len(otm.trustzones) == 1
        assert len(otm.components) == 22
        assert len(otm.dataflows) == 11

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, '804b664a-7129-4a9e-a08c-16a99669f605', public_cloud_type, 'Public Cloud')

        check_otm_component(otm, 0, 'ec2', 'Amazon EC2', '804b664a-7129-4a9e-a08c-16a99669f605')
        check_otm_component(otm, 9, 'vpc', 'Amazon VPC', '804b664a-7129-4a9e-a08c-16a99669f605')

        check_otm_dataflow(otm, 0, '1', '41')
        check_otm_dataflow(otm, 1, '6', '46')
        check_otm_dataflow(otm, 2, '11', '51')
        check_otm_dataflow(otm, 3, '16', '56')
        check_otm_dataflow(otm, 4, '21', '61')
        check_otm_dataflow(otm, 5, '26', '66')
        check_otm_dataflow(otm, 6, '31', '71')
        check_otm_dataflow(otm, 7, '36', '76')
        check_otm_dataflow(otm, 8, '97', '107')
        check_otm_dataflow(otm, 9, '102', '112')
        check_otm_dataflow(otm, 10, '120', '125')
