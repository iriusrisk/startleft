from startleft.diagram.visio_to_otm import VisioToOtm
from tests.resources import test_resource_paths
from tests.test_utils import TestUtils


class TestVisioDiagramToOtm:
    def test_diagram_to_otm(self):
        otm = VisioToOtm(test_resource_paths.visio_aws_with_tz_and_vpc).run()

        assert len(otm.trustzones) == 2
        assert len(otm.components) == 6
        assert len(otm.dataflows) == 4

        TestUtils.check_otm_trustzone(otm, 0, TestUtils.public_cloud_id, TestUtils.public_cloud_name)
        TestUtils.check_otm_trustzone(otm, 1, TestUtils.private_secured_id, TestUtils.private_secured_name)

        TestUtils.check_otm_component(otm, 0, 'empty-component', 'Custom VPC')
        TestUtils.check_otm_component(otm, 1, 'ec2', 'Amazon EC2')
        TestUtils.check_otm_component(otm, 2, 'ec2', 'Custom machine')
        TestUtils.check_otm_component(otm, 3, 'rds', 'Private Database')
        TestUtils.check_otm_component(otm, 4, 'cloudwatch', 'Amazon CloudWatch')
        TestUtils.check_otm_component(otm, 5, 'cloudwatch', 'Custom log system')

        TestUtils.check_otm_dataflow(otm, 0, '1', '12')
        TestUtils.check_otm_dataflow(otm, 1, '12', '30')
        TestUtils.check_otm_dataflow(otm, 2, '1', '35')
        TestUtils.check_otm_dataflow(otm, 3, '12', '41')
