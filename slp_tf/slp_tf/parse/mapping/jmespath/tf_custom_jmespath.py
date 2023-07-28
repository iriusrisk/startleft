import logging
from copy import deepcopy

import jmespath

import sl_util.sl_util.secure_regex as re
from slp_tf.slp_tf.parse.mapping.mappers.tf_base_mapper import generate_resource_identifier

logger = logging.getLogger(__name__)


def _adapt_dict(resource):
    """
    This function is an intern adapter method
    In a dictionary, will return a new copy with:
    1st Element value will be the value of the 1st element on the dictionary
    The rest element will be the same
    Example: {"aws_type":{x:y}, attributes} => {x:y, attributes}
    :param resource:
    :return:
    """
    if resource:
        new_element = {}
        for index, key in enumerate(resource):
            if index == 0:  # First element will be extracted
                new_element = deepcopy(resource[key])
            else:
                new_element[key] = resource[key]
        return new_element


def add_type_and_name(obj, component_type, component_name):
    new_obj = obj.copy()

    new_obj['Type'] = component_type
    new_obj['_key'] = component_name
    # Included with the purpose of maximize compatibility between mappings
    new_obj["resource_id"] = generate_resource_identifier(component_type, component_name)
    new_obj["resource_type"] = component_type
    new_obj['resource_name'] = component_name

    return new_obj


class TerraformCustomFunctions(jmespath.functions.Functions):
    @jmespath.functions.signature({'types': ['string']}, {'types': ['number']})
    def _func_tail(self, string, count):
        return string[-count:]

    @jmespath.functions.signature({'types': ['string']}, {'types': ['string']}, {'types': ['string', 'null']})
    def _func_re_sub(self, pattern, replace, s):
        s = s or ""
        return re.sub(pattern, replace, s)

    @jmespath.functions.signature({'types': ['array', 'null']})
    def _func_squash_terraform(self, component_types_arr):
        source_objects = []

        # Squash will include: resource_type, resource_name and resource_properties
        # with the purpose of maximize compatibility between mappings
        if component_types_arr is not None:
            for component_type_obj in component_types_arr:
                component_type, component_name_obj = list(component_type_obj.items())[0]
                source_object = {}
                if isinstance(component_name_obj, dict):
                    source_object["Type"] = component_type
                    source_object["resource_type"] = component_type
                    for component_name, properties in component_name_obj.items():
                        source_object["resource_id"] = generate_resource_identifier(component_type, component_name)
                        source_object["_key"] = component_name
                        source_object["resource_name"] = component_name
                        source_object["Properties"] = properties
                        source_object["resource_properties"] = properties
                source_objects.append(source_object)

        return source_objects

    @jmespath.functions.signature({'types': ['array', 'null']})
    def _func_adapt(self, resources):
        """
        This function is an adapter for the intern logic of slp_tf
        :param resources: An array of tf objects
        :return:
        """
        result = []
        if resources:
            for resource in resources:
                result.append(_adapt_dict(resource))
        return result

    @jmespath.functions.signature({'types': ['array', 'null']}, {'types': ['string']})
    def _func_get_starts_with(self, obj_arr, component_type):
        source_objects = []

        if obj_arr is not None:
            for obj in obj_arr:
                for c_type in obj:
                    if c_type.startswith(component_type):
                        for c_name in obj[c_type]:
                            new_obj = add_type_and_name(obj[c_type], c_type, c_name)
                            source_objects.append(new_obj)

        return source_objects

    @jmespath.functions.signature({'types': ['array', 'null']}, {'types': ['string']})
    def _func_get(self, obj_arr, component_type):
        source_objects = []

        if obj_arr is not None:
            for obj in obj_arr:
                for c_type in obj:
                    if c_type == component_type:
                        for c_name in obj[c_type]:
                            new_obj = add_type_and_name(obj[c_type], c_type, c_name)
                            source_objects.append(new_obj)

        return source_objects

    @jmespath.functions.signature({'types': ['array', 'null']}, {'types': ['string']})
    def _func_get_module_terraform(self, modules, module_type):
        source_objects = []

        if modules is not None:
            for module in modules:
                for c_type in module:
                    module_source = module[c_type]['source']
                    if module_source == module_type:
                        new_obj = add_type_and_name(module[c_type], module_source, c_type)
                        new_obj['module'] = True
                        source_objects.append(new_obj)

        return source_objects

    @jmespath.functions.signature({'types': ['string']}, {'types': ['string']})
    def _func_split(self, string, separator):
        return string.split(separator)

    @jmespath.functions.signature({'types': ['array', 'null']}, {'types': ['string']}, {'types': ['string']})
    def _func_regex(self, resources, key, regex):
        logger.debug(f"finding in {resources} with {key} and {regex}")
        result = []
        if resources:
            for resource in resources:
                if re.match(regex, resource.get(key)):
                    result.append(resource)
        return result


jmespath_options = jmespath.Options(custom_functions=TerraformCustomFunctions())


def jmespath_search(search_path, source):
    logger.debug(f"jmespath search with expression {search_path}")
    return jmespath.search(search_path, source, options=jmespath_options)
