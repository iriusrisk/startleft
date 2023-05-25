from unittest.mock import Mock

from pytest import raises

from slp_tfplan.slp_tfplan.transformers.dataflow.strategies.dataflow_creation_strategy import DataflowCreationStrategy, \
    DataflowCreationStrategyContainer
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
            instance.create_dataflows(otm=Mock(), relationships_extractor=Mock(), are_hierarchically_related=Mock())
