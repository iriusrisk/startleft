from typing import List
from unittest.mock import Mock

from pytest import mark, param

from slp_tf.slp_tf.tfplan.transformers.tfplan_dataflow_creator import TfplanDataflowCreator
from slp_tf.tests.unit.tfplan.otm_graph_util import build_mocked_otm, build_graph, build_mocked_tfplan_component
from slp_tf.slp_tf.tfplan.tfplan_objects import TfplanSecurityGroup, TfplanLaunchTemplate, TfplanComponent


class TestTfplanDataflowCreator:

    @mark.parametrize('components,security_groups', [
        param([Mock(id='mocked_component')], [], id='no_security_groups'),
        param([], [Mock(id='mocked_sg')], id='no_components'),
        param([Mock(id='mocked_component')], [Mock(id='mocked_sg')], id='unrelated_components_sgs'),
    ])
    def test_no_dataflows(self, components: List[TfplanComponent], security_groups: List[TfplanSecurityGroup]):
        # GIVEN an OTM with no SGs
        otm = build_mocked_otm(components=components, security_groups=security_groups)

        # AND a mock for the graph
        graph = build_graph([])

        # WHEN TfplanDataflowCreator::transform is invoked
        TfplanDataflowCreator(otm, graph).transform()

        # THEN no DFs are created in the OTM
        assert not otm.dataflows

    def test_sgs_and_components_loaded_and_related_by_graph(self):
        # GIVEN two SGs unrelated by configuration
        sg1 = TfplanSecurityGroup(security_group_id='sg1', ingress_sgs=[], egress_sgs=[])
        sg2 = TfplanSecurityGroup(security_group_id='sg2', ingress_sgs=[], egress_sgs=[])

        # AND two components
        component1 = build_mocked_tfplan_component({'component_name': 'c1', 'tf_type': 'c1-type'})
        component2 = build_mocked_tfplan_component({'component_name': 'c2', 'tf_type': 'c2-type'})

        # AND relationships between the components and their SGs
        c1_sg1_relationship = (component1.id, sg1.id)
        c2_sg2_relationship = (component2.id, sg2.id)

        # AND a relationship from the sg1 to the sg2
        sg1_sg2_relationship = (sg2.id, sg1.id)

        # AND a graph with those relationships
        graph = build_graph([
            c1_sg1_relationship,
            c2_sg2_relationship,
            sg1_sg2_relationship,
            (sg1.id, None)
        ])

        # AND an OTM with all those elements
        otm = build_mocked_otm(
            components=[component1, component2],
            security_groups=[sg1, sg2],
            launch_templates=[])

        # WHEN TfplanDataflowCreator::transform is invoked
        TfplanDataflowCreator(otm, graph).transform()

        # THEN a dataflow is created between the components
        assert len(otm.dataflows) == 1
        assert otm.dataflows[0].source_node == component1.id
        assert otm.dataflows[0].destination_node == component2.id

    def test_sgs_related_by_configuration_mixed_sg_component_association(self):
        # GIVEN two SGs related by configuration
        sg1 = TfplanSecurityGroup(security_group_id='sg1', ingress_sgs=[], egress_sgs=[])
        sg2 = TfplanSecurityGroup(security_group_id='sg2', ingress_sgs=['sg1'], egress_sgs=[])

        # AND two components
        component1 = build_mocked_tfplan_component({'component_name': 'c1', 'tf_type': 'c1-type'})
        component2 = build_mocked_tfplan_component({'component_name': 'c2', 'tf_type': 'c2-type'})

        # AND a launch template related with the first SG
        launch_template = TfplanLaunchTemplate(launch_template_id='lt1', security_groups_ids=['sg1'])

        # AND a graph that relates the launch template with the first component and the second with the second SG
        c1_lt1_relationship = (component1.id, launch_template.id)
        c2_sg2_relationship = (component2.id, sg2.id)

        graph = build_graph([
            c1_lt1_relationship,
            c2_sg2_relationship,
            (launch_template.id, None),
            (sg2.id, None)
        ])

        # AND an OTM with all those elements
        otm = build_mocked_otm(
            components=[component1, component2],
            security_groups=[sg1, sg2],
            launch_templates=[launch_template])

        # WHEN TfplanDataflowCreator::transform is invoked
        TfplanDataflowCreator(otm, graph).transform()

        # THEN a dataflow is created between the components
        assert len(otm.dataflows) == 1
        assert otm.dataflows[0].source_node == component1.id
        assert otm.dataflows[0].destination_node == component2.id
