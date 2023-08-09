from unittest.mock import Mock

from slp_tfplan.slp_tfplan.matcher import ComponentsAndSGsMatcher
from slp_tfplan.tests.util.builders import build_security_group_mock, build_mocked_otm, build_mocked_component

_component_a = build_mocked_component({
    'component_name': 'component_a',
    'tf_type': 'aws_type'
})

_component_b = build_mocked_component({
    'component_name': 'component_b',
    'tf_type': 'aws_type'
})

security_groups = [
    build_security_group_mock('SG1'),
    build_security_group_mock('SG2'),
    build_security_group_mock('SG3')
]


def are_component_in_sg(component, sg, relationships_extractor, launch_templates):
    # 'SG1' related to 'component_a' and 'component_b'
    # 'SG2' related to 'component_b'
    # 'SG3' not related to any component
    if component == _component_a and sg == security_groups[0]:
        return True
    elif component == _component_b and sg == security_groups[0]:
        return True
    elif component == _component_b and sg == security_groups[1]:
        return True
    return False


class TestComponentsAndSGsMatcher:

    def test_match(self):
        # GIVEN a list of components and a list of security groups

        otm = build_mocked_otm([_component_a, _component_b], security_groups=security_groups)

        # AND a matcher that returns the relationship between components and security groups
        components_and_sgs_matcher = ComponentsAndSGsMatcher(otm, Mock())
        components_and_sgs_matcher.are_component_in_sg = are_component_in_sg

        # WHEN matching components and security groups
        components_in_sgs = components_and_sgs_matcher.match()

        # THEN the result should be a dict with the security groups as keys and the components as values
        assert components_in_sgs == {
            security_groups[0].id: [_component_a, _component_b],
            security_groups[1].id: [_component_b]
        }
