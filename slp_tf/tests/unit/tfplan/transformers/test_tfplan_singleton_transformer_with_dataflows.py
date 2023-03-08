import pytest
from charset_normalizer.md import List

from otm.otm.entity.dataflow import Dataflow
from slp_tf.slp_tf.tfplan.tfplan_objects import TfplanComponent
from slp_tf.slp_tf.tfplan.transformers.tfplan_singleton_transformer import TfplanSingletonTransformer
from slp_tf.tests.unit.tfplan.otm_graph_util import build_mocked_tfplan_component, \
    build_mocked_dataflow, build_mocked_otm

_component_a = build_mocked_tfplan_component({
    'component_name': 'component_a',
    'tf_type': 'aws_type',
    'configuration': {"singleton": True}
})

_component_b = build_mocked_tfplan_component({
    'component_name': 'component_b',
    'tf_type': 'aws_type',
    'configuration': {"singleton": True}
})

_component_c = build_mocked_tfplan_component({
    'component_name': 'component_c',
    'tf_type': 'aws_type'
})

_dataflow_a_b = build_mocked_dataflow(_component_a, _component_b)
_dataflow_a_c = build_mocked_dataflow(_component_a, _component_c)
_dataflow_b_c = build_mocked_dataflow(_component_b, _component_c)
_dataflow_c_a = build_mocked_dataflow(_component_c, _component_a)
_dataflow_c_b = build_mocked_dataflow(_component_c, _component_b)

_dataflow_a_b_bidirectional = build_mocked_dataflow(_component_a, _component_b, bidirectional=True)
_dataflow_a_c_bidirectional = build_mocked_dataflow(_component_a, _component_c, bidirectional=True)
_dataflow_b_c_bidirectional = build_mocked_dataflow(_component_b, _component_c, bidirectional=True)
_dataflow_c_a_bidirectional = build_mocked_dataflow(_component_c, _component_a, bidirectional=True)
_dataflow_c_b_bidirectional = build_mocked_dataflow(_component_c, _component_b, bidirectional=True)


class TestTfplanSingletonTransformerWithDataflows:

    def test_component_to_component_dataflow(self):
        """
        Non singleton components (A) has dataflows to non singleton component (C)
        :return:
        """

        # GIVEN components with some dataflows
        otm = build_mocked_otm([_component_a, _component_c], [_dataflow_a_c])

        # WHEN TfplanSingletonTransformer::transform is invoked
        TfplanSingletonTransformer(otm).transform()

        # THEN nothing happens
        assert len(otm.dataflows) == 1
        assert otm.dataflows[0] == _dataflow_a_c

    @pytest.mark.parametrize('components, dataflows', [
        pytest.param([_component_a, _component_b, _component_c], [_dataflow_a_c, _dataflow_b_c], id="[A -> C, B -> C]"),
        pytest.param([_component_a, _component_b, _component_c], [_dataflow_a_c], id="[A -> C]"),
        pytest.param([_component_a, _component_b, _component_c], [_dataflow_b_c], id="[B -> C]")
    ])
    def test_singleton_to_component_dataflow(self, components: List[TfplanComponent], dataflows: List[Dataflow]):
        """
        Components singleton (A,B) has dataflows to C
        """

        # GIVEN components with some dataflows
        otm = build_mocked_otm(components, dataflows)

        # WHEN TfplanSingletonTransformer::transform is invoked
        TfplanSingletonTransformer(otm).transform()

        # THEN a unique dataflows exists between A -> C
        assert len(otm.dataflows) == 1
        assert otm.dataflows[0].source_node == _component_a.id
        assert otm.dataflows[0].destination_node == _component_c.id

    @pytest.mark.parametrize('components, dataflows', [
        pytest.param([_component_a, _component_b, _component_c], [_dataflow_c_a, _dataflow_c_b], id="[C -> A, C -> B]"),
        pytest.param([_component_a, _component_b, _component_c], [_dataflow_c_a], id="[C -> A]"),
        pytest.param([_component_a, _component_b, _component_c], [_dataflow_c_b], id="[C -> B]"),
    ])
    def test_component_to_singleton_dataflow(self, components: List[TfplanComponent], dataflows: List[Dataflow]):
        """
        Components C has dataflows to singleton (A,B)
        """

        # GIVEN components with some dataflows
        otm = build_mocked_otm(components, dataflows)

        # WHEN TfplanSingletonTransformer::transform is invoked
        TfplanSingletonTransformer(otm).transform()

        # THEN a unique dataflows exist between C -> A
        assert len(otm.dataflows) == 1
        assert otm.dataflows[0].source_node == _component_c.id
        assert otm.dataflows[0].destination_node == _component_a.id

    @pytest.mark.parametrize('components, dataflows', [
        pytest.param([_component_a, _component_b, _component_c],
                     [_dataflow_a_c_bidirectional, _dataflow_b_c_bidirectional], id="[A <-> C and B <-> C]"),
        pytest.param([_component_a, _component_b, _component_c],
                     [_dataflow_a_c_bidirectional, _dataflow_b_c], id="[A <-> C and B -> C]"),
        pytest.param([_component_a, _component_b, _component_c],
                     [_dataflow_a_c, _dataflow_b_c_bidirectional], id="[A -> C and B <-> C]"),
    ])
    def test_singleton_to_component_dataflow_bidirectional(
            self, components: List[TfplanComponent], dataflows: List[Dataflow]):
        """
        Components singleton (A,B) has some bidirectional dataflows to C
        """

        # GIVEN components with some dataflows
        otm = build_mocked_otm(components, dataflows)

        # WHEN TfplanSingletonTransformer::transform is invoked
        TfplanSingletonTransformer(otm).transform()

        # THEN a unique bidirectional dataflow exists between A -> C
        assert len(otm.dataflows) == 1
        assert otm.dataflows[0].source_node == _component_a.id
        assert otm.dataflows[0].destination_node == _component_c.id
        assert otm.dataflows[0].bidirectional is True

    @pytest.mark.parametrize('components, dataflows', [
        pytest.param([_component_a, _component_b, _component_c],
                     [_dataflow_c_a_bidirectional, _dataflow_c_b_bidirectional], id="[C <-> A and C <-> B]"),
        pytest.param([_component_a, _component_b, _component_c],
                     [_dataflow_c_a_bidirectional, _dataflow_c_b], id="[C <-> A and C -> B]"),
        pytest.param([_component_a, _component_b, _component_c],
                     [_dataflow_c_a, _dataflow_c_b_bidirectional], id="[C -> A and C <-> B]"),
    ])
    def test_component_to_singleton_dataflow_bidirectional(
            self, components: List[TfplanComponent], dataflows: List[Dataflow]):
        """
        Components C has some bidirectional dataflows to singleton (A,B)
        """

        # GIVEN components with some dataflows
        otm = build_mocked_otm(components, dataflows)

        # WHEN TfplanSingletonTransformer::transform is invoked
        TfplanSingletonTransformer(otm).transform()

        # THEN a unique bidirectional dataflow exists between C -> A
        assert len(otm.dataflows) == 1
        assert otm.dataflows[0].source_node == _component_c.id
        assert otm.dataflows[0].destination_node == _component_a.id
        assert otm.dataflows[0].bidirectional is True

    def test_singleton_dataflow_with_tags(self):
        """
        Components singleton (A,B) has some dataflows with tags to C
        """
        # GIVEN components with some dataflows with tags
        tag_1 = "tag_1"
        tag_2 = "tag_2"
        tag_3 = "tag_3"
        dataflows = [
            build_mocked_dataflow(_component_a, _component_c, tags=[tag_1, tag_2]),
            build_mocked_dataflow(_component_b, _component_c, tags=[tag_2, tag_3])
        ]
        otm = build_mocked_otm([_component_a, _component_b, _component_c], dataflows)

        # WHEN TfplanSingletonTransformer::transform is invoked
        TfplanSingletonTransformer(otm).transform()

        # THEN a unique bidirectional dataflow exists between A -> C with the following tags
        assert len(otm.dataflows) == 1
        assert otm.dataflows[0].source_node == _component_a.id
        assert otm.dataflows[0].destination_node == _component_c.id
        assert len(otm.dataflows[0].tags) == 3
        assert tag_1 in otm.dataflows[0].tags
        assert tag_2 in otm.dataflows[0].tags
        assert tag_3 in otm.dataflows[0].tags

    def test_singleton_dataflow_with_attributes(self):
        """
        Components singleton (A,B) has some dataflows with attributes to C
        """
        # GIVEN components with some dataflows with attributes
        attribute_1 = "attribute_1"
        attribute_2 = "attribute_2"
        attribute_3 = "attribute_3"
        dataflows = [
            build_mocked_dataflow(_component_a, _component_c, attributes=[attribute_1, attribute_2]),
            build_mocked_dataflow(_component_b, _component_c, attributes=[attribute_2, attribute_3])
        ]
        otm = build_mocked_otm([_component_a, _component_b, _component_c], dataflows)

        # WHEN TfplanSingletonTransformer::transform is invoked
        TfplanSingletonTransformer(otm).transform()

        # THEN a unique bidirectional dataflow exists between A -> C with the following attributes
        assert len(otm.dataflows) == 1
        assert otm.dataflows[0].source_node == _component_a.id
        assert otm.dataflows[0].destination_node == _component_c.id
        assert len(otm.dataflows[0].attributes) == 3
        assert attribute_1 in otm.dataflows[0].attributes
        assert attribute_2 in otm.dataflows[0].attributes
        assert attribute_3 in otm.dataflows[0].attributes
