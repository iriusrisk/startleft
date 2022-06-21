from startleft.diagram.diagram_type import DiagramType
from startleft.diagram.external_diagram_to_otm import ExternalDiagramToOtm
from startleft.utils.file_utils import FileUtils
from tests.resources import test_resource_paths
from tests.util.otm import check_otm_representations_size, check_otm_trustzone, check_otm_component,  \
    check_otm_dataflow, public_cloud_id, public_cloud_name, private_secured_id, private_secured_name


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

