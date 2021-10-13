from startleft import app
from tests.resources import test_resource_paths


class TestApp:

    def test_load_yaml_file(self):
        filename = test_resource_paths.example_yaml
        iac_to_otm = app.IacToOtmApp('name', 'id')
        iac_to_otm.load_yaml_source(filename)
        assert iac_to_otm.source_model.data

    def test_load_json_file(self):
        filename = test_resource_paths.example_json
        iac_to_otm = app.IacToOtmApp('name', 'id')
        iac_to_otm.load_yaml_source(filename)
        assert iac_to_otm.source_model.data

    def test_load_yaml_uploaded_file(self):
        filename = test_resource_paths.example_yaml
        iac_to_otm = app.IacToOtmApp('name', 'id')
        iac_to_otm.load_yaml_source(open(filename))
        assert iac_to_otm.source_model.data

    def test_load_json_uploaded_file(self):
        filename = test_resource_paths.example_json
        iac_to_otm = app.IacToOtmApp('name', 'id')
        iac_to_otm.load_yaml_source(open(filename))
        assert iac_to_otm.source_model.data
