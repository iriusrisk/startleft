from typing import Tuple
from unittest.mock import Mock

from pytest import mark, param

from slp_tfplan.slp_tfplan.matcher.component_security_group_match_strategies import \
    ComponentMatchStrategySecurityGroupByGraphStrategy


class TestComponentSecurityGroupByGraphStrategy:
    def test_no_graph_relationship_no_match(self):
        # GIVEN a mocked component
        component = Mock()

        # AND a mocked SecurityGroup
        security_group = Mock()

        # AND a relationships_extractor which returns no relationships between the component and the SG
        relationships_extractor = Mock()
        relationships_extractor.exist_valid_path = lambda c, sg: False

        # WHEN ComponentSecurityGroupByGraphStrategy::are_related is called
        result = ComponentMatchStrategySecurityGroupByGraphStrategy().are_related(
            component, security_group, relationships_extractor=relationships_extractor)

        # THEN the strategy returns False
        assert result == False

    @mark.parametrize('relationship', [
        param(('C', 'SG'), id='component to security group'),
        param(('SG', 'C'), id='security group to component')])
    def test_match_when_graph_relationship(self, relationship: Tuple[str]):
        # GIVEN a mocked component
        component = Mock(tf_resource_id='C')

        # AND a mocked SecurityGroup
        security_group = Mock(id='SG')

        # AND a relationship between the SG and the component in any direction
        relationships_extractor = Mock()
        relationships_extractor.exist_valid_path = lambda c, sg: (c, sg) == relationship

        # WHEN ComponentSecurityGroupByGraphStrategy::are_related is called
        result = ComponentMatchStrategySecurityGroupByGraphStrategy().are_related(
            component, security_group, relationships_extractor=relationships_extractor)

        # THEN the strategy returns True
        assert result == True

    # TODO include tests for error cases
