from random import randrange

from otm.otm.entity.parent_type import ParentType
from slp_tf.slp_tf.tfplan.transformers.tfplan_singleton_transformer import TfplanSingletonTransformer
from slp_tf.tests.unit.tfplan.otm_graph_util import DEFAULT_TRUSTZONE, build_otm_type, \
    build_mocked_tfplan_component, build_mocked_otm


def _merge_component_configurations(components) -> {}:
    merge_configuration = {}
    for component in components:
        merge_configuration = {**merge_configuration, **component.configuration}
    return merge_configuration


class TestTfplanSingletonTransformer:

    def test_none_components(self):
        """
        Given an otm without components
        """
        # GIVEN an OTM without components
        otm = build_mocked_otm([])
        # WHEN TfplanSingletonTransformer::transform is invoked
        TfplanSingletonTransformer(otm).transform()
        # THEN none exception is raised
        assert True

    def test_one_components_singleton(self):
        """
        Given an otm with a unique singleton component
        nothing should happen
        """

        # GIVEN an OTM with one component marked as singleton
        first_component = build_mocked_tfplan_component({
            'component_name': 'first_component',
            'tf_type': 'aws_type',
            'configuration': {"singleton": True}
        })

        otm = build_mocked_otm([first_component])

        # WHEN TfplanSingletonTransformer::transform is invoked
        TfplanSingletonTransformer(otm).transform()

        # THEN nothing happens
        assert len(otm.components) == 1
        assert otm.components[0] == first_component

    def test_singleton_is_parent(self):
        """
        Given an otm with three singleton (A,B,C) components with same type and parent
        But component 'C' is parent of non singleton component 'D'
        Singleton logic should unify only (A,B)
        """

        # Given an otm with three singleton (A,B,C) components with same type and parent
        # But component 'C' is parent of non singleton component 'D'

        component_a = build_mocked_tfplan_component({
            'component_name': 'component_a',
            'tf_type': 'aws_type',
            'configuration': {"singleton": True}
        })

        component_b = build_mocked_tfplan_component({
            'component_name': 'component_b',
            'tf_type': 'aws_type',
            'configuration': {"singleton": True}
        })

        component_c = build_mocked_tfplan_component({
            'component_name': 'component_c',
            'tf_type': 'aws_type',
            'configuration': {"singleton": True}
        })

        component_d = build_mocked_tfplan_component({
            'component_name': 'component_d',
            'tf_type': 'aws_type',
            'parent_id': component_c.id,
            'parent_type': ParentType.COMPONENT
        })

        otm = build_mocked_otm([component_a, component_b, component_c, component_d])

        # WHEN TfplanSingletonTransformer::transform is invoked
        TfplanSingletonTransformer(otm).transform()

        # THEN Singleton logic should unify only (A,B)
        assert len(otm.components) == 3
        assert otm.components[0].id == component_c.id
        assert otm.components[1].id == component_d.id
        assert otm.components[1].parent == component_c.id
        assert otm.components[1].parent_type == ParentType.COMPONENT
        assert otm.components[2].id == component_a.id

    def test_two_components_singleton_with_same_parents_and_none_dataflows(self):
        """
        Given an otm with two singleton components with same type and parent
        Singleton logic should unify them
        """

        # GIVEN an OTM with two components with same type/parent  marked as singleton
        tf_type = 'aws_type'
        component_type = build_otm_type(tf_type)
        component_configuration = {"singleton": True}

        first_component = build_mocked_tfplan_component({
            'component_name': 'first_component',
            'tf_type': tf_type,
            'component_type': component_type,
            'configuration': component_configuration
        })

        second_component = build_mocked_tfplan_component({
            'component_name': 'second_component',
            'tf_type': tf_type,
            'component_type': component_type,
            'configuration': component_configuration
        })

        components = [first_component, second_component]
        otm = build_mocked_otm(components)

        # WHEN TfplanSingletonTransformer::transform is invoked
        TfplanSingletonTransformer(otm).transform()

        expected_configuration = _merge_component_configurations(components)

        # THEN both componentes are merged into one with the following data
        assert len(otm.components) == 1
        assert otm.components[0].id == first_component.id
        assert otm.components[0].name == f'{component_type} (grouped)'
        assert otm.components[0].type == component_type
        assert otm.components[0].parent == DEFAULT_TRUSTZONE.id
        assert otm.components[0].parent_type == ParentType.TRUST_ZONE
        assert len(otm.components[0].tags) == 1
        assert otm.components[0].tags[0] == tf_type
        assert otm.components[0].tf_resource_id is None
        assert otm.components[0].tf_type is None
        assert otm.components[0].configuration == expected_configuration

    def test_two_components_singleton_with_different_parents_and_none_dataflows(self):
        """
        Given an otm with two singleton components with same type but different parent
        nothing should happen
        """

        # GIVEN an OTM with two components with same type and different parent marked as singleton
        tf_type = 'aws_type'
        component_configuration = {"singleton": True}

        first_component = build_mocked_tfplan_component({
            'component_name': 'first_component',
            'tf_type': tf_type,
            'parent_id': 'parent_id_1',
            'parent_type': 'parent_type_1',
            'configuration': component_configuration
        })

        second_component = build_mocked_tfplan_component({
            'component_name': 'second_component',
            'tf_type': tf_type,
            'parent_id': 'parent_id_2',
            'parent_type': 'parent_type_2',
            'configuration': component_configuration
        })

        otm = build_mocked_otm([first_component, second_component])

        # WHEN TfplanSingletonTransformer::transform is invoked
        TfplanSingletonTransformer(otm).transform()

        # THEN nothing happens
        assert len(otm.components) == 2
        assert otm.components[0] == first_component
        assert otm.components[1] == second_component

    def test_two_components_but_only_one_singleton_with_same_parents_and_none_dataflows(self):
        """
        Given an otm with two components with same type and parent but only one marked as singleton
        nothing should happen
        """

        # GIVEN an OTM with two components with same type/parent but only one marked as singleton
        tf_type = 'aws_type'

        first_component = build_mocked_tfplan_component({
            'component_name': 'first_component',
            'tf_type': tf_type,
            'configuration': {"singleton": True}
        })

        second_component = build_mocked_tfplan_component({
            'component_name': 'second_component',
            'tf_type': tf_type
        })

        otm = build_mocked_otm([first_component, second_component])

        # WHEN TfplanSingletonTransformer::transform is invoked
        TfplanSingletonTransformer(otm).transform()

        # THEN nothing happens
        assert len(otm.components) == 2
        assert otm.components[0] == first_component
        assert otm.components[1] == second_component

    def test_four_components_grouped_by_different_parents_and_none_dataflows(self):
        """
        Given an otm with four components having:
        * Two component with same parent_a and marked as singleton
        * Two other component with same parent_b and marked as singleton
        There should be two singleton component, one for each parent
        """

        # GIVEN an OTM with four components with same type/parent marked as singleton
        # grouped by two set of parents
        tf_type = 'aws_type'
        component_type = build_otm_type(tf_type)
        component_configuration = {"singleton": True}

        first_component_parent_a = build_mocked_tfplan_component({
            'component_name': 'first_component_parent_a',
            'tf_type': tf_type,
            'component_type': component_type,
            'parent_id': 'parent_id_a',
            'parent_type': 'parent_type_a',
            'configuration': component_configuration
        })

        second_component_parent_a = build_mocked_tfplan_component({
            'component_name': 'second_component_parent_a',
            'tf_type': tf_type,
            'component_type': component_type,
            'parent_id': 'parent_id_a',
            'parent_type': 'parent_type_a',
            'configuration': component_configuration
        })

        first_component_parent_b = build_mocked_tfplan_component({
            'component_name': 'first_component_parent_b',
            'tf_type': tf_type,
            'component_type': component_type,
            'parent_id': 'parent_id_b',
            'parent_type': 'parent_type_b',
            'configuration': component_configuration
        })

        second_component_parent_b = build_mocked_tfplan_component({
            'component_name': 'second_component_parent_b',
            'tf_type': tf_type,
            'component_type': component_type,
            'parent_id': 'parent_id_b',
            'parent_type': 'parent_type_b',
            'configuration': component_configuration
        })

        otm = build_mocked_otm([first_component_parent_a, second_component_parent_a,
                                first_component_parent_b, second_component_parent_b])

        # WHEN TfplanSingletonTransformer::transform is invoked
        TfplanSingletonTransformer(otm).transform()

        expected_configuration_parent_a \
            = _merge_component_configurations([first_component_parent_a, second_component_parent_a])
        expected_configuration_parent_b \
            = _merge_component_configurations([first_component_parent_b, second_component_parent_b])

        # THEN both componentes are merged into two with the following data
        assert len(otm.components) == 2
        assert otm.components[0].id == first_component_parent_a.id
        assert otm.components[0].name == f'{component_type} (grouped)'
        assert otm.components[0].type == component_type
        assert otm.components[0].parent == 'parent_id_a'
        assert otm.components[0].parent_type == 'parent_type_a'
        assert len(otm.components[0].tags) == 1
        assert otm.components[0].tags[0] == tf_type
        assert otm.components[0].tf_resource_id is None
        assert otm.components[0].tf_type is None
        assert otm.components[0].configuration == expected_configuration_parent_a

        assert otm.components[1].id == first_component_parent_b.id
        assert otm.components[1].name == f'{component_type} (grouped)'
        assert otm.components[1].type == component_type
        assert otm.components[1].parent == 'parent_id_b'
        assert otm.components[1].parent_type == 'parent_type_b'
        assert len(otm.components[1].tags) == 1
        assert otm.components[1].tags[0] == tf_type
        assert otm.components[1].tf_resource_id is None
        assert otm.components[1].tf_type is None
        assert otm.components[1].configuration == expected_configuration_parent_b

    def test_two_components_singleton_with_same_parents_different_tags_and_none_dataflows(self):
        """
        Given an otm with two singleton components with same type and parent but different tags
        Singleton logic should unify them and stack the tags
        """

        # GIVEN an OTM with two components with same type/parent marked as singleton
        # AND different tags
        component_type = 'component_type'
        component_configuration = {"singleton": True}
        tag_1 = "tag_1"
        tag_2 = "tag_2"
        tag_3 = "tag_3"

        first_component = build_mocked_tfplan_component({
            'component_name': 'first_component',
            'tf_type': 'first_aws_type',
            'component_type': component_type,
            'tags': [tag_1, tag_2],
            'configuration': component_configuration
        })

        second_component = build_mocked_tfplan_component({
            'component_name': 'second_component',
            'tf_type': 'second_aws_type',
            'component_type': component_type,
            'tags': [tag_2, tag_3],
            'configuration': component_configuration
        })

        components = [first_component, second_component]
        otm = build_mocked_otm(components)

        # WHEN TfplanSingletonTransformer::transform is invoked
        TfplanSingletonTransformer(otm).transform()

        expected_configuration = _merge_component_configurations(components)

        # THEN both componentes are merged into one with the following data and stack the tags
        assert len(otm.components) == 1
        assert otm.components[0].id == first_component.id
        assert otm.components[0].name == f'{component_type} (grouped)'
        assert otm.components[0].type == component_type
        assert otm.components[0].parent == DEFAULT_TRUSTZONE.id
        assert otm.components[0].parent_type == ParentType.TRUST_ZONE
        assert len(otm.components[0].tags) == 3
        assert tag_1 in otm.components[0].tags
        assert tag_2 in otm.components[0].tags
        assert tag_3 in otm.components[0].tags
        assert otm.components[0].tf_resource_id is None
        assert otm.components[0].tf_type is None
        assert otm.components[0].configuration == expected_configuration

    def test_random_number_of_singleton_components_with_same_parents(self):
        """
        Given an otm with a random number of singleton components with same type and parent
        Singleton logic should unify them
        """

        # GIVEN an otm with a random number of singleton components with same type and parent
        tf_type = 'aws_type'
        component_type = build_otm_type(tf_type)
        component_configuration = {"singleton": True}

        components = []
        for index in range(randrange(50)):
            components.append(build_mocked_tfplan_component(
                {
                    'component_name': f'component_{index}',
                    'tf_type': tf_type,
                    'component_type': component_type,
                    'configuration': component_configuration
                })
            )

        otm = build_mocked_otm(components)

        # WHEN TfplanSingletonTransformer::transform is invoked
        TfplanSingletonTransformer(otm).transform()

        expected_configuration = _merge_component_configurations(components)

        # THEN both componentes are merged into one with the following data
        assert len(otm.components) == 1
        assert otm.components[0].id == components[0].id
        assert otm.components[0].name == f'{component_type} (grouped)'
        assert otm.components[0].type == component_type
        assert otm.components[0].parent == DEFAULT_TRUSTZONE.id
        assert otm.components[0].parent_type == ParentType.TRUST_ZONE
        assert len(otm.components[0].tags) == 1
        assert otm.components[0].tags[0] == tf_type
        assert otm.components[0].tf_resource_id is None
        assert otm.components[0].tf_type is None
        assert otm.components[0].configuration == expected_configuration
