from typing import Union

from slp_tf.slp_tf.parse.mapping.jmespath.tf_custom_jmespath import jmespath_search


def __equals_condition(attribute, value):
    return f"{attribute} == '{value}'"


def __property_condition(attribute, value):
    return f"{attribute}.{value}"


def query(mapping_source, **kwargs):
    """
    Query functions for search through the entire source file data structure
    Those functions are:
        $type: find a resource by a type (or a list of types)
        $name: find a resource by a name (or a list of names)
        $props: find a resource by a props (or a list of props)
    :param mapping_source: The $source for a mapping component
    :param kwargs:
        source_model_data: The completely TF dictionary
    :return: The jmespath search of the composed query
    """
    source_model_data = kwargs.get("source_model_data", None)
    type_query = __generate_jmespath("resource_type", mapping_source.get("$type", None), __equals_condition)
    name_query = __generate_jmespath("resource_name", mapping_source.get("$name", None), __equals_condition)
    props_query = __generate_jmespath("resource_properties", mapping_source.get("$props", None), __property_condition)

    conditions = [type_query, name_query, props_query]
    return jmespath_search(__generate_full_path("resource", conditions), source_model_data)


def __generate_full_path(root, conditions):
    """
    Returns a full generated JMESPath by concatenating the different informed values with "|"
    :param root: Main root where to execute the query
    :param conditions: Conditions for generating the query
    :return: The full JMESPath Query for seeking in resources
    """
    return f"{root}|{'|'.join([elem for elem in conditions if elem])}|adapt(@)"


def __generate_jmespath(attribute: str, value: Union[dict, str, list], condition):
    """
    Initial method for handle conditional configurations for the query family functions
    if $regex is configured, a call to TerraformCustomFunctions._func_regex is configured on jmespath
    if list or string, a jmespath query is generated
    :param attribute:
    :param value:
    :param condition:
    :return:
    """
    if not value:
        return

    if isinstance(value, dict):
        if "$regex" in value:
            return __generate_jmespath_regex(attribute, value["$regex"])

    return __generate_jmespath_query(attribute, value, condition)


def __generate_jmespath_query(attribute: str, value: Union[str, list], condition):
    """
    Generates a JMESPath query with the following format: [[?$attribute=='$value'], ....]
    :param attribute: Left part of the condition
    :param value: Right part of the condition, if a list, it will be formatted following the MultiSelect List
    :return: A valid JMESPath Query
        Example:
            Single Element:     [?resource_type == 'aws_lb']
            Multiple Elements:  [?resource_type == 'aws_lb' || resource_type == 'aws_elb']
    """
    if not value:
        return

    if isinstance(value, str):
        value = [value]

    conditions = []
    for elem in value:
        conditions.append(condition(attribute, elem))
    return f"[?{' || '.join(conditions)}]" if len(conditions) > 0 else None


def __generate_jmespath_regex(attribute: str, value: str):
    return f"regex(@, '{attribute}', '{value}')"
