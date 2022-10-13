from otm.otm.otm import OTM
from slp_base import IacType
from slp_cft.slp_cft.parse.cft_parser import set_default_trustzone_for_unknown_component_parent
from slp_cft.tests.integration.test_cft_processor import DEFAULT_TRUSTZONE_ID


class TestCloudformationParser:

    def test_set_default_trustzone_for_unknown_component_parent(self):
        otm: OTM = OTM("project_id", "project_name", IacType.CLOUDFORMATION)

        otm.add_component("id_0", "component", "type", "not_found_id", "component")
        otm.add_component("id_1", "component", "type", DEFAULT_TRUSTZONE_ID, "trustZone")
        otm.add_component("id_2", "component", "type", "id_1", "component")

        set_default_trustzone_for_unknown_component_parent(otm)

        assert filter(lambda component: component.id == "id_0" and
                                        component.parent == DEFAULT_TRUSTZONE_ID and
                                        component.parent_type == "component", otm.components)
        assert filter(lambda component: component.id == "id_1" and
                                component.parent == DEFAULT_TRUSTZONE_ID and
                                component.parent_type == "trustZone", otm.components)
        assert filter(lambda component: component.id == "id_2" and
                                        component.parent == "id_1" and
                                        component.parent_type == "component", otm.components)
