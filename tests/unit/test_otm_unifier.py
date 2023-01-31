import json

from otm.otm.entity.component import OtmComponent
from otm.otm.entity.trustzone import OtmTrustzone
from otm.otm.otm_builder import OtmBuilder
from otm.otm.provider import Provider
from sl_util.sl_util.file_utils import get_data
from slp_base.slp_base.otm_trustzone_unifier import OtmTrustZoneUnifier
from tests.resources.test_resource_paths import MTMT_multiple_trustzones_same_type_ID


class DummyType(str, Provider):
    DUMMY = ("DUMMY", "Dummy", "diagram")


class TestOtmUnifier:

    def test_api_diagram_controller_happy_path(self):
        # GIVEN an otm with multiple trust zones with the same type
        trustzones: [OtmTrustzone] = [
            OtmTrustzone(trustzone_id='60e82972', type='6376d53e', name='Internet'),
            OtmTrustzone(trustzone_id='250a69a4', type='6376d53e', name='Public'),
            OtmTrustzone(trustzone_id='d6987386', type='6376d53e', name='Intranet'),
            OtmTrustzone(trustzone_id='e85a8516', type='6376d53e', name='Private'),
            OtmTrustzone(trustzone_id='75163eca', type='b61d6911', name='Public Cloud Zone'),
        ]
        components: [OtmComponent] = [
            OtmComponent('de588d55', 'Public Web App', '', '250a69a4', 'trustZone'),
            OtmComponent('6460a14f', 'Browser', '', '60e82972', 'trustZone'),
            OtmComponent('348d1acd', 'Web API', '', 'd6987386', 'trustZone'),
            OtmComponent('9c7e2caa', 'Intranet Web App', '', 'd6987386', 'trustZone'),
            OtmComponent('104c3e42', 'PostgreSQL', '', 'e85a8516', 'trustZone'),
            OtmComponent('a2986e26', 'DynamoDB', '', '75163eca', 'trustZone'),

        ]
        origin = OtmBuilder('test1', 'Test 1', DummyType.DUMMY).add_trustzones(trustzones).add_components(components) \
            .build()

        # AND the expected otm without tz type field
        expected = json.loads(get_data(MTMT_multiple_trustzones_same_type_ID))

        # WHEN we unify the trust zones
        OtmTrustZoneUnifier(origin).unify()

        # THEN we check the expected result
        assert origin.json() == expected

