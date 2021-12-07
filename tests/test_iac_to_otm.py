from startleft.iac_to_otm import IacToOtm
from tests.resources import test_resource_paths


class TestApp:

    def test_load_yaml_file(self):
        filename = test_resource_paths.example_yaml
        iac_to_otm = IacToOtm('name', 'id')
        iac_to_otm.load_yaml_source(filename)
        assert iac_to_otm.source_model.data

    def test_load_json_file(self):
        filename = test_resource_paths.example_json
        iac_to_otm = IacToOtm('name', 'id')
        iac_to_otm.load_yaml_source(filename)
        assert iac_to_otm.source_model.data

    def test_load_yaml_uploaded_file(self):
        filename = test_resource_paths.example_yaml
        iac_to_otm = IacToOtm('name', 'id')
        iac_to_otm.load_yaml_source(open(filename))
        assert iac_to_otm.source_model.data

    def test_load_json_uploaded_file(self):
        filename = test_resource_paths.example_json
        iac_to_otm = IacToOtm('name', 'id')
        iac_to_otm.load_yaml_source(open(filename))
        assert iac_to_otm.source_model.data

    def test_run(self):
        filename = test_resource_paths.example_json
        mapping_filename = test_resource_paths.default_mapping
        iac_to_otm = IacToOtm('name', 'id')
        iac_to_otm.run('Cloudformation', mapping_filename, 'threatmodel.otm', filename)
        assert iac_to_otm.source_model.data

    def test_run_cloudformation_mappings(self):
        filename = test_resource_paths.cloudformation_for_mappings_tests_json
        mapping_filename = test_resource_paths.default_mapping
        iac_to_otm = IacToOtm('name', 'id')
        iac_to_otm.run('Cloudformation', mapping_filename, 'threatmodel.otm', filename)
        assert iac_to_otm.source_model.otm
        assert len(iac_to_otm.source_model.otm.trustzones) == 1
        assert len(iac_to_otm.source_model.otm.components) > 1
