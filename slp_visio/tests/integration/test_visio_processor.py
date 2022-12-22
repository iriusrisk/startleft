from sl_util.sl_util.file_utils import get_data
from slp_base.tests.util.otm import check_otm_representations_size, check_otm_trustzone, public_cloud_id, \
    public_cloud_name, check_otm_component, check_otm_dataflow, private_secured_id, private_secured_name, internet_id, \
    internet_name
from slp_visio.slp_visio.visio_processor import VisioProcessor
from slp_visio.tests.resources import test_resource_paths


class TestVisioProcessor:
    def test_empty_mapping_file(self):
        visio_file = open(test_resource_paths.visio_aws_shapes, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.empty_mapping)],
        ).process()

        assert len(otm.trustzones) == 0
        assert len(otm.components) == 0
        assert len(otm.dataflows) == 0

    def test_empty_visio_file(self):
        visio_file = open(test_resource_paths.visio_empty, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.default_visio_mapping)],
        ).process()

        assert len(otm.trustzones) == 1
        assert len(otm.components) == 0
        assert len(otm.dataflows) == 0
        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_name)

    def test_empty_mapping_and_visio_files(self):
        visio_file = open(test_resource_paths.visio_empty, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.empty_mapping)],
        ).process()

        assert len(otm.trustzones) == 0
        assert len(otm.components) == 0
        assert len(otm.dataflows) == 0

    def test_aws_shapes(self):
        visio_file = open(test_resource_paths.visio_aws_shapes, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.default_visio_mapping)],
        ).process()

        assert len(otm.trustzones) == 1
        assert len(otm.components) == 5
        assert len(otm.dataflows) == 4

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_name)

        check_otm_component(otm, 0, 'ec2', 'Amazon-EC2')
        check_otm_component(otm, 1, 'ec2', 'Custom-machine')
        check_otm_component(otm, 2, 'rds', 'Private-Database')
        check_otm_component(otm, 3, 'cloudwatch', 'Amazon-CloudWatch')
        check_otm_component(otm, 4, 'cloudwatch', 'Custom-log-system')

        check_otm_dataflow(otm, 0, '1', '12')
        check_otm_dataflow(otm, 1, '12', '30')
        check_otm_dataflow(otm, 2, '1', '35')
        check_otm_dataflow(otm, 3, '12', '41')

    def test_generic_elements(self):
        visio_file = open(test_resource_paths.visio_generic_shapes, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.custom_vpc_mapping)],
        ).process()

        assert len(otm.trustzones) == 1
        assert len(otm.components) == 2
        assert len(otm.dataflows) == 1

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_name)

        check_otm_component(otm, 0, 'empty-component', 'Custom-enterprise-GW')
        check_otm_component(otm, 1, 'empty-component', 'Custom-web-server')

    def test_self_pointing_connectors(self):
        visio_file = open(test_resource_paths.visio_self_pointing_connectors, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.custom_vpc_mapping)],
        ).process()

        assert len(otm.trustzones) == 1
        assert len(otm.components) == 2
        assert len(otm.dataflows) == 0

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_name)

        check_otm_component(otm, 0, 'empty-component', 'Custom-enterprise-GW')
        check_otm_component(otm, 1, 'empty-component', 'Custom-web-server')

    def test_extraneous_elements(self):
        visio_file = open(test_resource_paths.visio_extraneous_elements, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.default_visio_mapping)],
        ).process()

        assert len(otm.trustzones) == 2
        assert len(otm.components) == 5
        assert len(otm.dataflows) == 4

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_name)
        check_otm_trustzone(otm, 1, private_secured_id, private_secured_name)

        check_otm_component(otm, 0, 'ec2', 'Amazon-EC2')
        check_otm_component(otm, 1, 'ec2', 'Custom-machine')
        check_otm_component(otm, 2, 'rds', 'Private-Database')
        check_otm_component(otm, 3, 'cloudwatch', 'Amazon-CloudWatch')
        check_otm_component(otm, 4, 'cloudwatch', 'Custom-log-system')

        check_otm_dataflow(otm, 0, '1', '12')
        check_otm_dataflow(otm, 1, '12', '30')
        check_otm_dataflow(otm, 2, '1', '35')
        check_otm_dataflow(otm, 3, '12', '41')

    def test_simple_boundary_tzs(self):
        visio_file = open(test_resource_paths.visio_simple_boundary_tzs, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.default_visio_mapping)],
        ).process()

        assert len(otm.trustzones) == 2
        assert len(otm.components) == 2
        assert len(otm.dataflows) == 1

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_name)
        check_otm_trustzone(otm, 1, private_secured_id, private_secured_name)

        check_otm_component(otm, 0, 'ec2', 'Custom-machine', 'b61d6911-338d-46a8-9f39-8dcd24abfe91')
        check_otm_component(otm, 1, 'rds', 'Private-Database', '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d')

        check_otm_dataflow(otm, 0, '12', '30')

    def test_boundary_tz_and_default_tz(self):
        visio_file = open(test_resource_paths.visio_boundary_tz_and_default_tz, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.default_visio_mapping)],
        ).process()

        assert len(otm.trustzones) == 2
        assert len(otm.components) == 2
        assert len(otm.dataflows) == 1

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, private_secured_id, private_secured_name)
        check_otm_trustzone(otm, 1, public_cloud_id, public_cloud_name)

        check_otm_component(otm, 0, 'ec2', 'Custom-machine', 'b61d6911-338d-46a8-9f39-8dcd24abfe91')
        check_otm_component(otm, 1, 'rds', 'Private-Database', '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d')

        check_otm_dataflow(otm, 0, '12', '30')

    def test_overlapped_boundary_tzs(self):
        visio_file = open(test_resource_paths.visio_overlapped_boundary_tzs, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.default_visio_mapping)],
        ).process()

        assert len(otm.trustzones) == 2
        assert len(otm.components) == 2
        assert len(otm.dataflows) == 1

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_name)
        check_otm_trustzone(otm, 1, private_secured_id, private_secured_name)

        check_otm_component(otm, 0, 'ec2', 'Custom-machine', 'b61d6911-338d-46a8-9f39-8dcd24abfe91')
        check_otm_component(otm, 1, 'rds', 'Private-Database', '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d')

        check_otm_dataflow(otm, 0, '12', '30')

    def test_visio_boundary_and_component_tzs(self):
        visio_file = open(test_resource_paths.visio_boundary_and_component_tzs, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.default_visio_mapping)],
        ).process()

        assert len(otm.trustzones) == 3
        assert len(otm.components) == 2
        assert len(otm.dataflows) == 1

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, internet_id, internet_name)
        check_otm_trustzone(otm, 1, private_secured_id, private_secured_name)
        check_otm_trustzone(otm, 2, public_cloud_id, public_cloud_name)

        check_otm_component(otm, 0, 'ec2', 'Custom-machine', 'f0ba7722-39b6-4c81-8290-a30a248bb8d9')
        check_otm_component(otm, 1, 'rds', 'Private-Database', '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d')

        check_otm_dataflow(otm, 0, '12', '30')

    def test_multiple_pages_diagram(self):
        visio_file = open(test_resource_paths.visio_multiple_pages_diagram, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.default_visio_mapping)],
        ).process()

        assert len(otm.trustzones) == 3
        assert len(otm.components) == 3
        assert len(otm.dataflows) == 2

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_name)
        check_otm_trustzone(otm, 1, private_secured_id, private_secured_name)
        check_otm_trustzone(otm, 2, internet_id, internet_name)

        check_otm_component(otm, 0, 'ec2', 'Custom-machine', 'b61d6911-338d-46a8-9f39-8dcd24abfe91')
        check_otm_component(otm, 1, 'rds', 'Private-Database', '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d')
        check_otm_component(otm, 2, 'ec2', 'Internet-Machine', 'f0ba7722-39b6-4c81-8290-a30a248bb8d9')

        check_otm_dataflow(otm, 0, '12', '30')
        check_otm_dataflow(otm, 1, '65', '30')

    def test_complex_diagram(self):
        visio_file = open(test_resource_paths.visio_aws_with_tz_and_vpc, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.default_visio_mapping)],
        ).process()

        assert len(otm.trustzones) == 2
        assert len(otm.components) == 5
        assert len(otm.dataflows) == 4

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_name)
        check_otm_trustzone(otm, 1, private_secured_id, private_secured_name)

        check_otm_component(otm, 0, 'ec2', 'Amazon-EC2')
        check_otm_component(otm, 1, 'ec2', 'Custom-machine')
        check_otm_component(otm, 2, 'rds', 'Private-Database')
        check_otm_component(otm, 3, 'cloudwatch', 'Amazon-CloudWatch')
        check_otm_component(otm, 4, 'cloudwatch', 'Custom-log-system')

        check_otm_dataflow(otm, 0, '1', '12')
        check_otm_dataflow(otm, 1, '12', '30')
        check_otm_dataflow(otm, 2, '1', '35')
        check_otm_dataflow(otm, 3, '12', '41')

    def test_prune_orphan_connectors(self):
        visio_file = open(test_resource_paths.visio_orphan_dataflows, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.default_visio_mapping)],
        ).process()

        assert len(otm.trustzones) == 1
        assert len(otm.components) == 6
        assert len(otm.dataflows) == 5

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_name)

        check_otm_component(otm, 0, 's3', 'Bucket')
        check_otm_component(otm, 1, 's3', 'Bucket')
        check_otm_component(otm, 2, 'CD-MQ', 'Amazon-MQ')
        check_otm_component(otm, 3, 'CD-MQ', 'Amazon-MQ')
        check_otm_component(otm, 4, 'rds', 'Database')
        check_otm_component(otm, 5, 'CD-MQ', 'Amazon-MQ')

        check_otm_dataflow(otm, 0, '31', '19')
        check_otm_dataflow(otm, 1, '46', '19')
        check_otm_dataflow(otm, 2, '99', '19')
        check_otm_dataflow(otm, 3, '99', '86')
        check_otm_dataflow(otm, 4, '46', '13')

    def test_bidirectional_connectors(self):
        visio_file = open(test_resource_paths.visio_bidirectional_connectors, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.default_visio_mapping)],
        ).process()

        assert len(otm.trustzones) == 1
        assert len(otm.components) == 6
        assert len(otm.dataflows) == 3

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_name)

        check_otm_component(otm, 0, 'ec2', 'Amazon-EC2', 'b61d6911-338d-46a8-9f39-8dcd24abfe91')
        check_otm_component(otm, 1, 'ec2', 'Amazon-EC2', 'b61d6911-338d-46a8-9f39-8dcd24abfe91')
        check_otm_component(otm, 2, 'ec2', 'Amazon-EC2', 'b61d6911-338d-46a8-9f39-8dcd24abfe91')
        check_otm_component(otm, 3, 'vpc', 'Amazon-VPC', 'b61d6911-338d-46a8-9f39-8dcd24abfe91')
        check_otm_component(otm, 4, 'vpc', 'Amazon-VPC', 'b61d6911-338d-46a8-9f39-8dcd24abfe91')
        check_otm_component(otm, 5, 'vpc', 'Amazon-VPC', 'b61d6911-338d-46a8-9f39-8dcd24abfe91')

        check_otm_dataflow(otm, 0, '23', '1', True)
        check_otm_dataflow(otm, 1, '28', '6', True)
        check_otm_dataflow(otm, 2, '33', '17', True)

    def test_manually_modified_connectors(self):
        visio_file = open(test_resource_paths.visio_modified_single_connectors, "r")
        otm = VisioProcessor(
            "project-id",
            "project-name",
            visio_file,
            [get_data(test_resource_paths.default_visio_mapping)],
        ).process()

        assert len(otm.trustzones) == 1
        assert len(otm.components) == 22
        assert len(otm.dataflows) == 11

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_name)

        check_otm_component(otm, 0, 'ec2', 'Amazon-EC2', 'b61d6911-338d-46a8-9f39-8dcd24abfe91')
        check_otm_component(otm, 9, 'vpc', 'Amazon-VPC', 'b61d6911-338d-46a8-9f39-8dcd24abfe91')

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
