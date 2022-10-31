import json

from deepmerge import always_merger

from slp_tf.slp_tf.parse.mapping.jmespath.tf_custom_jmespath import jmespath_search
from slp_tf.slp_tf.parse.mapping.search.tf_mapping_function_selector import MappingFunctionSelector


class TerraformSourceModel:
    def __init__(self, data=None, otm=None):
        self.data = data or {}
        self.otm = otm
        self.lookup = {}
        self.mapping_function_selector = MappingFunctionSelector()

    def load(self, data):
        always_merger.merge(self.data, data)

    def json(self):
        return json.dumps(self.data, indent=2)

    def query(self, query):
        return jmespath_search(query, self.data)

    def search(self, mapping_source, source=None):
        if isinstance(mapping_source, str):
            return mapping_source

        if isinstance(mapping_source, list):
            results = []
            for element in mapping_source:
                mapping_path_value = self.search(element, source)
                if isinstance(mapping_path_value, list):
                    results = results + mapping_path_value
                else:
                    results = results + [str(mapping_path_value)]
            return results

        if isinstance(mapping_source, dict):

            if mapping_function := self.mapping_function_selector.get(mapping_source):
                return mapping_function(
                    mapping_source=mapping_source, tf_source_model=self, source=source, source_model_data=self.data)

            return mapping_source
