from unittest.mock import Mock

from pytest import mark, param

from slp_tfplan.slp_tfplan.matcher.strategies.sg_sg_match_strategies import \
    SecurityGroupByGraphStrategy, SecurityGroupByConfigurationStrategy
from slp_tfplan.slp_tfplan.objects.tfplan_objects import SecurityGroup


class TestSecurityGroupByConfigurationStrategy:

    def test_unrelated_sgs(self):
        # GIVEN two mocked SGs no referenced among them in the configuration
        security_group_1 = Mock(id='SG1', ingress_sgs=[], egress_sgs=[])
        security_group_2 = Mock(id='SG2', ingress_sgs=[], egress_sgs=[])

        # WHEN SecurityGroupByConfigurationStrategy::are_related is called
        result = SecurityGroupByConfigurationStrategy().are_related(security_group_1, security_group_2)

        # THEN the strategy returns False
        assert result is False

    @mark.parametrize('source_security_group,target_security_group', [
        param(Mock(id='SG1', ingress_sgs=[], egress_sgs=[]), Mock(id='SG2', ingress_sgs=['SG1'], egress_sgs=[]),
              id='source id in target ingress'),
        param(Mock(id='SG1', ingress_sgs=[], egress_sgs=['SG2']), Mock(id='SG2', ingress_sgs=[], egress_sgs=[]),
              id='target id in source egress')
    ])
    def test_related_sgs(self, source_security_group: SecurityGroup, target_security_group: SecurityGroup):
        # GIVEN two related SGs

        # WHEN SecurityGroupByConfigurationStrategy::are_related is called
        result = SecurityGroupByConfigurationStrategy().are_related(source_security_group, target_security_group)

        # THEN the strategy returns True
        assert result is True


class TestSecurityGroupByGraphStrategy:

    def test_no_graph_relationship_no_match(self):
        # GIVEN any two mocked SGs
        mocked_sgs = [Mock(), Mock()]

        # AND a relationships_extractor which returns no relationships between them
        relationships_extractor = Mock()
        relationships_extractor.exist_valid_path = lambda sg_a, sg_b: False

        # WHEN SecurityGroupByGraphStrategy::are_related is called
        result = SecurityGroupByGraphStrategy() \
            .are_related(*mocked_sgs, relationships_extractor=relationships_extractor)

        # THEN the strategy returns False
        assert result is False

    def test_match_when_graph_relationship(self):
        # GIVEN two mocked security groups SG1 and SG2
        security_group_1 = Mock(id='SG1')
        security_group_2 = Mock(id='SG2')

        # AND a mocked relationship from SG2 to SG1
        relationships_extractor = Mock()
        relationships_extractor.exist_valid_path = lambda sg_a, sg_b: (sg_a, sg_b) == ('SG2', 'SG1')

        # WHEN SecurityGroupByGraphStrategy::are_related is called
        result = SecurityGroupByGraphStrategy().are_related(
            security_group_1, security_group_2, relationships_extractor=relationships_extractor)

        # THEN the strategy returns True
        assert result is True
