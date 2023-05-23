from unittest.mock import Mock

from slp_tfplan.slp_tfplan.matcher.strategies.component_security_group_match_strategies import \
    ComponentSecurityGroupByLaunchTemplateStrategyMatchStrategy


class TestComponentSecurityGroupByLaunchTemplateStrategy:
    def test_no_launch_template_relationship_no_match(self):
        # GIVEN a mocked component
        component = Mock()

        # AND a mocked SecurityGroup
        security_group = Mock()

        # AND no launch templates
        launch_templates = []

        # AND a relationships_extractor which returns no relationships between the component and the SG
        relationships_extractor = Mock()
        relationships_extractor.exist_valid_path = lambda c, sg: False

        # WHEN ComponentSecurityGroupByLaunchTemplateStrategy::are_related is called
        result = ComponentSecurityGroupByLaunchTemplateStrategyMatchStrategy().are_related(component,
                                                                                           security_group,
                                                                                           relationships_extractor=relationships_extractor,
                                                                                           launch_templates=launch_templates)

        # THEN the strategy returns False
        assert result == False

    def test_match_when_launch_template_sg_relationship(self):
        # GIVEN a mocked component
        component = Mock(tf_resource_id='C')

        # AND a mocked SecurityGroup
        security_group = Mock(id='SG')

        # AND a launch template related with the SecurityGroup
        launch_template = Mock(id='LT', security_groups_ids=[security_group.id])

        # AND a relationship between the component and the launch template
        relationships_extractor = Mock()
        relationships_extractor.exist_valid_path = lambda c, lt: (c, lt) == (component.tf_resource_id, launch_template.id)

        # WHEN ComponentSecurityGroupByLaunchTemplateStrategy::are_related is called
        result = ComponentSecurityGroupByLaunchTemplateStrategyMatchStrategy().are_related(component,
                                                                                           security_group,
                                                                                           relationships_extractor=relationships_extractor,
                                                                                           launch_templates=[launch_template])

        # THEN the strategy returns True
        assert result == True

    # TODO include tests for error cases
