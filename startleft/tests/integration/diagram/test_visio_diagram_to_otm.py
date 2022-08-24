from sl_util.sl_util import file_utils as FileUtils
from slp_base import DiagramType
from slp_base.tests.util.otm import check_otm_representations_size, check_otm_trustzone, check_otm_component, \
    check_otm_dataflow, public_cloud_id, public_cloud_name, private_secured_id, private_secured_name, internet_name, \
    internet_id
from startleft.startleft.diagram.external_diagram_to_otm import ExternalDiagramToOtm
from startleft.tests.resources import test_resource_paths


class TestVisioDiagramToOtm:
    def test_aws_shapes(self):
        otm = ExternalDiagramToOtm(DiagramType.VISIO).run(
            test_resource_paths.visio_aws_shapes,
            [FileUtils.get_data(test_resource_paths.default_visio_mapping)],
            "project-name",
            "project-id"
        )

        assert len(otm.trustzones) == 1
        assert len(otm.components) == 5
        assert len(otm.dataflows) == 4

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_name)

        check_otm_component(otm, 0, 'ec2', 'Amazon EC2')
        check_otm_component(otm, 1, 'ec2', 'Custom machine')
        check_otm_component(otm, 2, 'rds', 'Private Database')
        check_otm_component(otm, 3, 'cloudwatch', 'Amazon CloudWatch')
        check_otm_component(otm, 4, 'cloudwatch', 'Custom log system')

        check_otm_dataflow(otm, 0, '1', '12')
        check_otm_dataflow(otm, 1, '12', '30')
        check_otm_dataflow(otm, 2, '1', '35')
        check_otm_dataflow(otm, 3, '12', '41')

    def test_generic_elements(self):
        otm = ExternalDiagramToOtm(DiagramType.VISIO).run(
            test_resource_paths.visio_generic_shapes,
            [FileUtils.get_data(test_resource_paths.custom_vpc_mapping)],
            "project-name",
            "project-id"
        )

        assert len(otm.trustzones) == 1
        assert len(otm.components) == 2
        assert len(otm.dataflows) == 1

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_name)

        check_otm_component(otm, 0, 'empty-component', 'Custom enterprise GW')
        check_otm_component(otm, 1, 'empty-component', 'Custom web server')

    def test_self_pointing_connectors(self):
        otm = ExternalDiagramToOtm(DiagramType.VISIO).run(
            test_resource_paths.visio_self_pointing_connectors,
            [FileUtils.get_data(test_resource_paths.custom_vpc_mapping)],
            "project-name",
            "project-id"
        )

        assert len(otm.trustzones) == 1
        assert len(otm.components) == 2
        assert len(otm.dataflows) == 0

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_name)

        check_otm_component(otm, 0, 'empty-component', 'Custom enterprise GW')
        check_otm_component(otm, 1, 'empty-component', 'Custom web server')

    def test_extraneous_elements(self):
        otm = ExternalDiagramToOtm(DiagramType.VISIO).run(
            test_resource_paths.visio_extraneous_elements,
            [FileUtils.get_data(test_resource_paths.default_visio_mapping)],
            "project-name",
            "project-id"
        )

        assert len(otm.trustzones) == 2
        assert len(otm.components) == 5
        assert len(otm.dataflows) == 4

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_name)
        check_otm_trustzone(otm, 1, private_secured_id, private_secured_name)

        check_otm_component(otm, 0, 'ec2', 'Amazon EC2')
        check_otm_component(otm, 1, 'ec2', 'Custom machine')
        check_otm_component(otm, 2, 'rds', 'Private Database')
        check_otm_component(otm, 3, 'cloudwatch', 'Amazon CloudWatch')
        check_otm_component(otm, 4, 'cloudwatch', 'Custom log system')

        check_otm_dataflow(otm, 0, '1', '12')
        check_otm_dataflow(otm, 1, '12', '30')
        check_otm_dataflow(otm, 2, '1', '35')
        check_otm_dataflow(otm, 3, '12', '41')

    def test_simple_boundary_tzs(self):
        otm = ExternalDiagramToOtm(DiagramType.VISIO).run(
            test_resource_paths.visio_simple_boundary_tzs,
            [FileUtils.get_data(test_resource_paths.default_visio_mapping)],
            "project-name",
            "project-id"
        )

        assert len(otm.trustzones) == 2
        assert len(otm.components) == 2
        assert len(otm.dataflows) == 1

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_name)
        check_otm_trustzone(otm, 1, private_secured_id, private_secured_name)

        check_otm_component(otm, 0, 'ec2', 'Custom machine', 'b61d6911-338d-46a8-9f39-8dcd24abfe91')
        check_otm_component(otm, 1, 'rds', 'Private Database', '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d')

        check_otm_dataflow(otm, 0, '12', '30')

    def test_boundary_tz_and_default_tz(self):
        otm = ExternalDiagramToOtm(DiagramType.VISIO).run(
            test_resource_paths.visio_boundary_tz_and_default_tz,
            [FileUtils.get_data(test_resource_paths.default_visio_mapping)],
            "project-name",
            "project-id"
        )

        assert len(otm.trustzones) == 2
        assert len(otm.components) == 2
        assert len(otm.dataflows) == 1

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_name)
        check_otm_trustzone(otm, 1, private_secured_id, private_secured_name)

        check_otm_component(otm, 0, 'ec2', 'Custom machine', 'b61d6911-338d-46a8-9f39-8dcd24abfe91')
        check_otm_component(otm, 1, 'rds', 'Private Database', '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d')

        check_otm_dataflow(otm, 0, '12', '30')

    def test_overlapped_boundary_tzs(self):
        otm = ExternalDiagramToOtm(DiagramType.VISIO).run(
            test_resource_paths.visio_overlapped_boundary_tzs,
            [FileUtils.get_data(test_resource_paths.default_visio_mapping)],
            "project-name",
            "project-id"
        )

        assert len(otm.trustzones) == 2
        assert len(otm.components) == 2
        assert len(otm.dataflows) == 1

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_name)
        check_otm_trustzone(otm, 1, private_secured_id, private_secured_name)

        check_otm_component(otm, 0, 'ec2', 'Custom machine', 'b61d6911-338d-46a8-9f39-8dcd24abfe91')
        check_otm_component(otm, 1, 'rds', 'Private Database', '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d')

        check_otm_dataflow(otm, 0, '12', '30')

    def test_visio_boundary_and_component_tzs(self):
        otm = ExternalDiagramToOtm(DiagramType.VISIO).run(
            test_resource_paths.visio_boundary_and_component_tzs,
            [FileUtils.get_data(test_resource_paths.default_visio_mapping)],
            "project-name",
            "project-id"
        )

        assert len(otm.trustzones) == 3
        assert len(otm.components) == 2
        assert len(otm.dataflows) == 1

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_name)
        check_otm_trustzone(otm, 1, internet_id, internet_name)
        check_otm_trustzone(otm, 2, private_secured_id, private_secured_name)

        check_otm_component(otm, 0, 'ec2', 'Custom machine', 'f0ba7722-39b6-4c81-8290-a30a248bb8d9')
        check_otm_component(otm, 1, 'rds', 'Private Database', '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d')

        check_otm_dataflow(otm, 0, '12', '30')

    def test_nested_tzs(self):
        otm = ExternalDiagramToOtm(DiagramType.VISIO).run(
            test_resource_paths.visio_nested_tzs,
            [FileUtils.get_data(test_resource_paths.default_visio_mapping)],
            "project-name",
            "project-id"
        )

        assert len(otm.trustzones) == 2
        assert len(otm.components) == 2
        assert len(otm.dataflows) == 1

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_name)
        check_otm_trustzone(otm, 1, private_secured_id, private_secured_name)

        check_otm_component(otm, 0, 'ec2', 'Custom machine', 'f0ba7722-39b6-4c81-8290-a30a248bb8d9')
        check_otm_component(otm, 1, 'rds', 'Private Database', '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d')

        check_otm_dataflow(otm, 0, '12', '30')

    def test_multiple_pages_diagram(self):
        otm = ExternalDiagramToOtm(DiagramType.VISIO).run(
            test_resource_paths.visio_multiple_pages_diagram,
            [FileUtils.get_data(test_resource_paths.default_visio_mapping)],
            "project-name",
            "project-id"
        )

        assert len(otm.trustzones) == 3
        assert len(otm.components) == 3
        assert len(otm.dataflows) == 2

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_name)
        check_otm_trustzone(otm, 1, private_secured_id, private_secured_name)
        check_otm_trustzone(otm, 2, internet_id, internet_name)

        check_otm_component(otm, 0, 'ec2', 'Custom machine', 'b61d6911-338d-46a8-9f39-8dcd24abfe91')
        check_otm_component(otm, 1, 'rds', 'Private Database', '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d')
        check_otm_component(otm, 2, 'ec2', 'Internet Machine', 'f0ba7722-39b6-4c81-8290-a30a248bb8d9')

        check_otm_dataflow(otm, 0, '12', '30')
        check_otm_dataflow(otm, 1, '65', '30')

    def test_complex_diagram(self):
        otm = ExternalDiagramToOtm(DiagramType.VISIO).run(
            test_resource_paths.visio_aws_with_tz_and_vpc,
            [FileUtils.get_data(test_resource_paths.default_visio_mapping)],
            "project-name",
            "project-id"
        )

        assert len(otm.trustzones) == 2
        assert len(otm.components) == 5
        assert len(otm.dataflows) == 4

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_name)
        check_otm_trustzone(otm, 1, private_secured_id, private_secured_name)

        check_otm_component(otm, 0, 'ec2', 'Amazon EC2')
        check_otm_component(otm, 1, 'ec2', 'Custom machine')
        check_otm_component(otm, 2, 'rds', 'Private Database')
        check_otm_component(otm, 3, 'cloudwatch', 'Amazon CloudWatch')
        check_otm_component(otm, 4, 'cloudwatch', 'Custom log system')

        check_otm_dataflow(otm, 0, '1', '12')
        check_otm_dataflow(otm, 1, '12', '30')
        check_otm_dataflow(otm, 2, '1', '35')
        check_otm_dataflow(otm, 3, '12', '41')

    def test_prune_orphan_connectors(self):
        otm = ExternalDiagramToOtm(DiagramType.VISIO).run(
            test_resource_paths.visio_orphan_dataflows,
            [FileUtils.get_data(test_resource_paths.default_visio_mapping)],
            "project-name",
            "project-id"
        )

        assert len(otm.trustzones) == 1
        assert len(otm.components) == 6
        assert len(otm.dataflows) == 5

        check_otm_representations_size(otm)

        check_otm_trustzone(otm, 0, public_cloud_id, public_cloud_name)

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

