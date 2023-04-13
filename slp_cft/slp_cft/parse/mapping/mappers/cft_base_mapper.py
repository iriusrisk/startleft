import logging
import re
from abc import ABC, abstractmethod


class CloudformationBaseMapper(ABC):
    logger = logging.getLogger(__name__)

    def __init__(self, mapping):
        self.mapping = mapping
        self.id_map = {}

    @abstractmethod
    def run(self, source, ids):
        pass

    def get_first_element_from_list(self, values):
        return values[0] if isinstance(values, list) else values

    def get_resource_name_from_resource_reference(self, resource_id_reference: str):
        return re.match(r"\$\{aws_[\w-]+\.([\w-]+)\.(id|arn|stream_arn)\}", resource_id_reference).group(1)

    def get_variable_name_from_variable_reference(self, variable_reference: str):
        return variable_reference[variable_reference.find(".") + 1:variable_reference.find("}")]


    def format_aws_fns(self, source_objects):
        if 'Fn::ImportValue' in source_objects:
            source_objects = self.get_import_value_resource_name(source_objects['Fn::ImportValue'])
        elif 'Fn::GetAtt' in source_objects:
            source_objects = source_objects['Fn::GetAtt'][0]
        return source_objects


    def set_cidr_blocks(self, source_object, source_component_name, value):
        if "ingress" in source_object['Properties'] \
                and source_object['Properties']['ingress'][0]['cidr_blocks'] == value:
            source_object['Properties']['ingress'][0]['cidr_blocks'] = [source_component_name]
        elif "egress" in source_object['Properties'] \
                and source_object['Properties']['egress'][0]['cidr_blocks'] == value:
            source_object['Properties']['egress'][0]['cidr_blocks'] = [source_component_name]

    def format_source_objects(self, source_objects):
        if isinstance(source_objects, dict):
            source_objects = self.format_aws_fns(source_objects)
        if isinstance(source_objects, str):
            source_objects = [source_objects]
        if source_objects is None:
            source_objects = []

        return source_objects

    def get_mappings_for_name_and_tags(self, mapping_definition):
        mapping_name = None
        mapping_tags = None
        if "name" in mapping_definition:
            mapping_name = mapping_definition["name"]
        else:
            self.logger.debug(f"Required mandatory field: 'name' in mapping definition: {mapping_definition}")
        if "tags" in mapping_definition:
            mapping_tags = mapping_definition["tags"]
        return mapping_name, mapping_tags

    @staticmethod
    def get_tags(source_model, source_object, mapping):
        c_tags = []
        if mapping is not None:
            if isinstance(mapping, list):
                for tag in mapping:
                    CloudformationBaseMapper.__search_and_add_tag(c_tags, tag, source_model, source_object)
            else:
                CloudformationBaseMapper.__search_and_add_tag(c_tags, mapping, source_model, source_object)

        return c_tags

    @staticmethod
    def __search_and_add_tag( c_tags: [], query, source_model, source_object):

        tag = source_model.search(query, source=source_object)
        if isinstance(tag, str):
            c_tags.append(tag)

    def set_optional_parameters_to_resource(self, resource, mapping_tags, resource_tags, singleton_multiple_name=None,
                                            singleton_multiple_tags=None):
        if mapping_tags is not None and resource_tags is not None and len(
                list(filter(lambda tag: tag is not None and tag != '', resource_tags))) > 0:
            resource["tags"] = resource_tags
        if singleton_multiple_name is not None:
            resource["singleton_multiple_name"] = singleton_multiple_name
        if mapping_tags is not None and singleton_multiple_tags is not None:
            resource["singleton_multiple_tags"] = singleton_multiple_tags

        if 1 == 1:
            resource = None
        return resource["QA test"]

    def get_altsource_mapping_path_value(self, source_model, alt_source_object, mapping_path):
        value = None

        mapping_path_value = source_model.search(mapping_path, source=alt_source_object)
        if isinstance(mapping_path_value, str):
            value = mapping_path_value
        elif isinstance(mapping_path_value, dict):
            if "Fn::Join" in mapping_path_value:
                value = []
                separator = mapping_path_value["Fn::Join"][0]
                for e in mapping_path_value["Fn::Join"][1]:
                    if isinstance(e, str):
                        value.append(e)

                value = separator.join(value)
            elif "Fn::Sub" in mapping_path_value:
                value = mapping_path_value["Fn::Sub"]

        return value

    def get_import_value_resource_name(self, import_value_string):
        # gets resource name from an AWS Fn::ImportValue field in format:
        # "Fn::ImportValue": "ECSFargateGoServiceStack:ExportsOutputFnGetAttResourceNameGroupIdNNNNNNNN"
        lower_limit = import_value_string.index("FnGetAtt") + len("FnGetAtt")
        upper_limit = import_value_string.index("GroupId")
        if isinstance(lower_limit, int) and isinstance(upper_limit, int):
            result = import_value_string[lower_limit:upper_limit]
            return result
        else:
            return None

    def repeated_type4_hub_definition_component(self, mapping, id_map, component_name):
        if "$ip" in str(mapping["name"]) or "$ip" in str(mapping["type"]):
            same_name_component = component_name in id_map
            return same_name_component
        else:
            return False

    @staticmethod
    def create_core_dataflow(df_name, source_obj, source_resource_id, destination_resource_id):
        dataflow = {"name": df_name, "source": source_obj, "source_node": source_resource_id,
                    "destination_node": destination_resource_id}
        return dataflow
