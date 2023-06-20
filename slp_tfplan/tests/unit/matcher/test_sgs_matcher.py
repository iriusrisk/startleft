from collections import Counter
from unittest.mock import Mock

from slp_tfplan.slp_tfplan.matcher import SGsMatcher
from slp_tfplan.tests.util.builders import build_security_group_mock, build_mocked_otm

sg_1 = build_security_group_mock('SG1')
sg_2 = build_security_group_mock('SG2')
sg_3 = build_security_group_mock('SG3')

security_groups = [sg_1, sg_2, sg_3]


def are_sgs_related(resource_1, resource_2, **kwargs):
    # 'SG1' related to 'SG2' and 'SG3'
    # 'SG2' related to 'SG3'
    # 'SG3' not related to any sg
    if resource_1 == sg_1 and resource_2 in (sg_2, sg_3):
        return True
    elif resource_1 == sg_2 and resource_2 == sg_3:
        return True
    return False


class TestSGsMatcher:

    def test_sg_match(self):
        # GIVEN a list of security groups
        # AND a matcher that returns the relationship between security groups
        otm = build_mocked_otm(components=[], security_groups=security_groups)
        sgs_matcher = SGsMatcher(otm, Mock())
        sgs_matcher.are_sgs_related = are_sgs_related

        # WHEN matching security groups
        sgs_relationships = sgs_matcher.match()

        # THEN the result should be a dict with the security groups as keys and the related security groups as values
        assert Counter(sgs_relationships[sg_1.id]) == Counter([sg_2.id, sg_3.id])
        assert sgs_relationships[sg_2.id] == [sg_3.id]
