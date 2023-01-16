import logging
import re
import uuid
from abc import ABC, abstractmethod

from slp_tf.slp_tf.parse.mapping.mappers.tf_backward_compatibility import TfIdMapDictionary


def is_terraform_resource_reference(value: str):
    return value is not None and isinstance(value, str) and re.match(
        r"\$\{aws_[\w-]+\.[\w-]+\.(id|arn|stream_arn)\}", value)


def get_resource_id_from_resource_reference(resource_id_reference: str):
    return re.match(r"\$\{(aws_[\w-]+\.[\w-]+)\.(id|arn|stream_arn)\}", resource_id_reference).group(1)


def generate_resource_identifier(resource_type, resource_name):
    return f"{resource_type}.{resource_name}"


class TerraformBaseMapper(ABC):
    logger = logging.getLogger(__name__)

    def __init__(self, mapping):
        self.mapping = mapping
        self.id_map = TfIdMapDictionary()

    @abstractmethod
    def run(self, source, ids):
        pass

    def get_first_element_from_list(self, values):
        return values[0] if isinstance(values, list) else values

    def is_terraform_variable_reference(self, value: str):
        return value is not None and isinstance(value, str) and re.match(r"\$\{var\.[\w-]+\}", value)

    def get_variable_name_from_variable_reference(self, variable_reference: str):
        return variable_reference[variable_reference.find(".") + 1:variable_reference.find("}")]

    def get_terraform_variable_default_value(self, source_model, variable_reference):
        name = self.get_variable_name_from_variable_reference(variable_reference)

        for variable in source_model.data["variable"]:
            for variable_name, variable_properties in variable.items():
                if variable_name == name:
                    return source_model.data[name][0] if name in source_model.data else variable_properties["default"][0]

    def format_terraform_variable(self, source_model, source_object, value):
        source_component_name = self.get_terraform_variable_default_value(source_model, value)
        self.set_cidr_blocks(source_object, source_component_name, value)
        return source_component_name

    def set_cidr_blocks(self, source_object, source_component_name, value):
        for xxgress in ["ingress", "egress"]:
            if source_object.get('resource_properties', {}).get(xxgress, [{}])[0].get('cidr_blocks', {}) == value:
                source_object['resource_properties'][xxgress][0]['cidr_blocks'] = [source_component_name]
                source_object['Properties'][xxgress][0]['cidr_blocks'] = [source_component_name]  # deprecated

    def format_source_objects(self, source_objects):
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
                    TerraformBaseMapper.__search_and_add_tag(c_tags, tag, source_model, source_object)
            else:
                TerraformBaseMapper.__search_and_add_tag(c_tags, mapping, source_model, source_object)

        return c_tags

    @staticmethod
    def __search_and_add_tag(c_tags: [], query, source_model, source_object):

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

        return resource

    def get_altsource_mapping_path_value(self, source_model, alt_source_object, mapping_path):
        value = None

        mapping_path_value = source_model.search(mapping_path, source=alt_source_object)
        if isinstance(mapping_path_value, str):
            value = mapping_path_value

        return value

    def repeated_type4_hub_definition_component(self, mapping, component_resource_id):
        if "$ip" in str(mapping["name"]) or "$ip" in str(mapping["type"]):
            return component_resource_id in self.id_map

    # if exists an aws_vpc which cidr_block value is the component["id"]
    # Prevent to generate component and map on id_map the component["id"] to the aws_vpc uuid
    # for Dataflow generation
    def exists_vpc_with_cidr_block_in_id_map(self, source_model, component_resource_id):
        for resource in source_model.query(
                "resource|[?resource_type=='aws_vpc' && resource_properties.cidr_block]"):
            cidr_block = resource['resource_properties']['cidr_block']
            if self.is_terraform_variable_reference(cidr_block):
                cidr_block = self.get_terraform_variable_default_value(source_model, cidr_block)
            if cidr_block == component_resource_id:
                aws_vpc_component_id = self.id_map.get(
                    generate_resource_identifier(resource["resource_type"], resource["resource_name"]), None)
                if aws_vpc_component_id:
                    self.id_map[component_resource_id] = aws_vpc_component_id
                    return True

    @staticmethod
    def create_core_dataflow(df_name, source_obj, source_resource_id, destination_resource_id):
        dataflow = {"id": str(uuid.uuid4()), "name": df_name, "source": source_obj, "source_node": source_resource_id,
                    "destination_node": destination_resource_id}
        return dataflow
