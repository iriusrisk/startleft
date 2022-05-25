from startleft.diagram.diagram_type import DiagramType
from startleft.diagram.external_diagram_to_otm import ExternalDiagramToOtm
from tests.resources import test_resource_paths
from tests.test_utils import TestUtils


class TestVisioDiagramToOtm:
    def test_aws_shapes(self):
        otm = ExternalDiagramToOtm(DiagramType.VISIO).run(
            test_resource_paths.visio_aws_shapes,
            open(test_resource_paths.default_visio_mapping, 'rb'),
            "project-name",
            "project-id"
        )

        assert len(otm.trustzones) == 1
        assert len(otm.components) == 5
        assert len(otm.dataflows) == 4

        TestUtils.check_otm_representations_size(otm)

        TestUtils.check_otm_trustzone(otm, 0, TestUtils.public_cloud_id, TestUtils.public_cloud_name)

        TestUtils.check_otm_component(otm, 0, 'ec2', 'Amazon EC2')
        TestUtils.check_otm_component(otm, 1, 'ec2', 'Custom machine')
        TestUtils.check_otm_component(otm, 2, 'rds', 'Private Database')
        TestUtils.check_otm_component(otm, 3, 'cloudwatch', 'Amazon CloudWatch')
        TestUtils.check_otm_component(otm, 4, 'cloudwatch', 'Custom log system')

        TestUtils.check_otm_dataflow(otm, 0, '1', '12')
        TestUtils.check_otm_dataflow(otm, 1, '12', '30')
        TestUtils.check_otm_dataflow(otm, 2, '1', '35')
        TestUtils.check_otm_dataflow(otm, 3, '12', '41')

    def test_generic_elements(self):
        otm = ExternalDiagramToOtm(DiagramType.VISIO).run(
            test_resource_paths.visio_generic_shapes,
            open(test_resource_paths.custom_vpc_mapping, 'rb'),
            "project-name",
            "project-id"
        )

        assert len(otm.trustzones) == 1
        assert len(otm.components) == 2
        assert len(otm.dataflows) == 1

        TestUtils.check_otm_representations_size(otm)

        TestUtils.check_otm_trustzone(otm, 0, TestUtils.public_cloud_id, TestUtils.public_cloud_name)

        TestUtils.check_otm_component(otm, 0, 'empty-component', 'Custom enterprise GW')
        TestUtils.check_otm_component(otm, 1, 'empty-component', 'Custom web server')

    def test_self_pointing_connectors(self):
        otm = ExternalDiagramToOtm(DiagramType.VISIO).run(
            test_resource_paths.visio_self_pointing_connectors,
            open(test_resource_paths.custom_vpc_mapping, 'rb'),
            "project-name",
            "project-id"
        )

        assert len(otm.trustzones) == 1
        assert len(otm.components) == 2
        assert len(otm.dataflows) == 0

        TestUtils.check_otm_representations_size(otm)

        TestUtils.check_otm_trustzone(otm, 0, TestUtils.public_cloud_id, TestUtils.public_cloud_name)

        TestUtils.check_otm_component(otm, 0, 'empty-component', 'Custom enterprise GW')
        TestUtils.check_otm_component(otm, 1, 'empty-component', 'Custom web server')

    def test_extraneous_elements(self):
        otm = ExternalDiagramToOtm(DiagramType.VISIO).run(
            test_resource_paths.visio_extraneous_elements,
            open(test_resource_paths.default_visio_mapping, 'rb'),
            "project-name",
            "project-id"
        )

        assert len(otm.trustzones) == 2
        assert len(otm.components) == 5
        assert len(otm.dataflows) == 4

        TestUtils.check_otm_representations_size(otm)

        TestUtils.check_otm_trustzone(otm, 0, TestUtils.public_cloud_id, TestUtils.public_cloud_name)
        TestUtils.check_otm_trustzone(otm, 1, TestUtils.private_secured_id, TestUtils.private_secured_name)

        TestUtils.check_otm_component(otm, 0, 'ec2', 'Amazon EC2')
        TestUtils.check_otm_component(otm, 1, 'ec2', 'Custom machine')
        TestUtils.check_otm_component(otm, 2, 'rds', 'Private Database')
        TestUtils.check_otm_component(otm, 3, 'cloudwatch', 'Amazon CloudWatch')
        TestUtils.check_otm_component(otm, 4, 'cloudwatch', 'Custom log system')

        TestUtils.check_otm_dataflow(otm, 0, '1', '12')
        TestUtils.check_otm_dataflow(otm, 1, '12', '30')
        TestUtils.check_otm_dataflow(otm, 2, '1', '35')
        TestUtils.check_otm_dataflow(otm, 3, '12', '41')

    def test_complex_diagram(self):
        otm = ExternalDiagramToOtm(DiagramType.VISIO).run(
            test_resource_paths.visio_aws_with_tz_and_vpc,
            open(test_resource_paths.default_visio_mapping, 'rb'),
            "project-name",
            "project-id"
        )

        assert len(otm.trustzones) == 2
        assert len(otm.components) == 5
        assert len(otm.dataflows) == 4

        TestUtils.check_otm_representations_size(otm)

        TestUtils.check_otm_trustzone(otm, 0, TestUtils.public_cloud_id, TestUtils.public_cloud_name)
        TestUtils.check_otm_trustzone(otm, 1, TestUtils.private_secured_id, TestUtils.private_secured_name)

        TestUtils.check_otm_component(otm, 0, 'ec2', 'Amazon EC2')
        TestUtils.check_otm_component(otm, 1, 'ec2', 'Custom machine')
        TestUtils.check_otm_component(otm, 2, 'rds', 'Private Database')
        TestUtils.check_otm_component(otm, 3, 'cloudwatch', 'Amazon CloudWatch')
        TestUtils.check_otm_component(otm, 4, 'cloudwatch', 'Custom log system')

        TestUtils.check_otm_dataflow(otm, 0, '1', '12')
        TestUtils.check_otm_dataflow(otm, 1, '12', '30')
        TestUtils.check_otm_dataflow(otm, 2, '1', '35')
        TestUtils.check_otm_dataflow(otm, 3, '12', '41')

