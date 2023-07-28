from unittest.mock import Mock

from pytest import raises, mark, param

from slp_tfplan.slp_tfplan.transformers.dataflow.strategies.dataflow_creation_strategy import DataflowCreationStrategy, \
    DataflowCreationStrategyContainer, create_dataflow
from slp_tfplan.tests.util.builders import get_instance_classes


class TestDataflowCreationStrategy:

    def test_get_strategies(self):
        # GIVEN all the subclasses of the DataflowCreationStrategy interface
        dataflow_creation_strategy_subclasses = DataflowCreationStrategy.__subclasses__()

        # AND the DataflowCreationStrategyContainer
        dataflow_creation_strategy_container = DataflowCreationStrategyContainer()

        # AND all the instances for DataflowCreationStrategyContainer strategies
        dataflow_creation_strategy_instances = get_instance_classes(dataflow_creation_strategy_container.strategies)

        # THEN the subclasses and the instances match
        assert dataflow_creation_strategy_subclasses == dataflow_creation_strategy_instances

    def test_interface_instantiated_error(self):
        # GIVEN an instance of the interface itself
        instance = DataflowCreationStrategy()

        # WHEN DataflowCreationStrategy::create_dataflows is called
        # THEN an NotImplementedError is raised
        with raises(NotImplementedError):
            instance.create_dataflows(otm=Mock(), relationships_extractor=Mock())

    @mark.parametrize('source_id,source_name,target_id,target_name,bidirectional,expected_id,expected_name', [
        param('1', 'C1', '2', 'C2', False, '465a886e-6345-4dc1-90dd-05b94067c641', 'C1 to C2',
              id='simple dataflow'),
        param('2', 'C2', '1', 'C1', True, '6e4a6b08-a58d-4a0c-a070-57df888afd35', 'C2 to C1 (bidirectional)',
              id='bidirectional dataflow')
    ])
    def test_create_dataflow(self,
                             source_id: str,
                             source_name: str,
                             target_id: str,
                             target_name: str,
                             bidirectional: bool,
                             expected_id: str,
                             expected_name: str):
        # GIVEN a source component
        source_component = Mock(id=source_id)
        source_component.name = source_name

        # AND a target component ID and name
        target_component = Mock(id=target_id)
        target_component.name = target_name

        # AND a bidirectional flag

        # WHEN create_dataflow is invoked
        dataflow = create_dataflow(source_component, target_component, bidirectional=bidirectional)

        # THEN a dataflow is created with the right ID
        assert dataflow.id == expected_id

        # AND its name is right
        assert dataflow.name == expected_name

        # AND its source_node is the ID of the source component
        assert dataflow.source_node == source_id

        # AND its destination_node node is the ID of the destination_node component
        assert dataflow.destination_node == target_id

        # AND its bidirectional flag is set right
        assert dataflow.bidirectional == bidirectional

    def test_create_dataflow_bidirectional_same_id(self):
        # GIVEN two components
        component_1 = Mock(id='1')
        component_1.name = 'C1'

        component_2 = Mock(id='2')
        component_2.name = 'C2'

        # AND a bidirectional flag set to True
        bidirectional = True

        # WHEN create_dataflow with the components in the two directions
        dataflow_1 = create_dataflow(component_1, component_2, bidirectional=bidirectional)
        dataflow_2 = create_dataflow(component_2, component_1, bidirectional=bidirectional)

        # THEN the ID for the two dataflows is the same
        assert dataflow_1.id == dataflow_2.id
