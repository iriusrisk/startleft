class TestUtils:
    public_cloud_id = 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
    public_cloud_name = 'Public Cloud'

    private_secured_id = '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'
    private_secured_name = 'Private Secured'

    @staticmethod
    def check_otm_trustzone(otm, position, trustzone_id, name):
        assert otm.trustzones[position].id == trustzone_id
        assert otm.trustzones[position].name == name

    @staticmethod
    def check_otm_component(otm, position, component_type, name, parent=None, tags=[]):
        assert otm.components[position].type == component_type
        assert otm.components[position].name == name

        if parent:
            assert otm.components[position].parent == parent

        for c_tag in tags:
            assert c_tag in otm.components[position].tags

    @staticmethod
    def check_otm_dataflow(otm, position, source_node, destination_node):
        assert otm.dataflows[position].source_node == source_node
        assert otm.dataflows[position].destination_node == destination_node

    @staticmethod
    def check_otm_representations_size(otm):
        assert "size" in otm.json()["representations"][0].keys()
        assert "width" in otm.json()["representations"][0]["size"].keys()
        assert "height" in otm.json()["representations"][0]["size"].keys()
