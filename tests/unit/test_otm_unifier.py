import json

from otm.otm.entity.component import Component
from otm.otm.entity.representation import RepresentationType
from otm.otm.entity.trustzone import Trustzone
from otm.otm.otm_builder import OTMBuilder
from otm.otm.provider import Provider
from sl_util.sl_util.file_utils import get_byte_data
from slp_base.slp_base.otm_trustzone_unifier import OTMTrustZoneUnifier
from tests.resources.test_resource_paths import MTMT_multiple_trustzones_same_type_ID


class DummyType(str, Provider):
    DUMMY = ("DUMMY", "Dummy", RepresentationType.DIAGRAM)


class TestOTMUnifier:

    def test_multiple_trustzones_same_type(self):
        # GIVEN an otm with multiple trust zones with the same type
        trustzones: [Trustzone] = [
            Trustzone(trustzone_id='60e82972', type='6376d53e', name='Internet'),
            Trustzone(trustzone_id='250a69a4', type='6376d53e', name='Public'),
            Trustzone(trustzone_id='d6987386', type='6376d53e', name='Intranet'),
            Trustzone(trustzone_id='e85a8516', type='6376d53e', name='Private'),
            Trustzone(trustzone_id='75163eca', type='b61d6911', name='Public Cloud Zone'),
        ]
        components: [Component] = [
            Component('de588d55', 'Public Web App', '', '250a69a4', 'trustZone'),
            Component('6460a14f', 'Browser', '', '60e82972', 'trustZone'),
            Component('348d1acd', 'Web API', '', 'd6987386', 'trustZone'),
            Component('9c7e2caa', 'Intranet Web App', '', 'd6987386', 'trustZone'),
            Component('104c3e42', 'PostgreSQL', '', 'e85a8516', 'trustZone'),
            Component('a2986e26', 'DynamoDB', '', '75163eca', 'trustZone'),

        ]
        origin = OTMBuilder('test1', 'Test 1', DummyType.DUMMY).add_trustzones(trustzones).add_components(components) \
            .build()

        # AND the expected otm without tz type field
        expected = json.loads(get_byte_data(MTMT_multiple_trustzones_same_type_ID))

        # WHEN we unify the trust zones
        OTMTrustZoneUnifier(origin).unify()

        # THEN we check the expected result
        assert origin.json() == expected

