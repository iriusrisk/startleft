from typing import List, Dict


# TODO Consider migrating these functions to use jmespath

def _get_resource_properties_expressions(resource: {}) -> Dict:
    return resource['resource_properties'].get('expressions', {})


def _get_referenced_resources(references: List[str]):
    valid_references = []

    for reference in references:
        if not reference.split('.')[-1] == 'id':
            valid_references.append(reference)

    return valid_references


def _get_value_from_expressions(resource: Dict, path: List[str]):
    expressions = _get_resource_properties_expressions(resource)
    if not expressions:
        return []

    source = expressions
    for i, element in enumerate(path):
        source = source.get(element)
        if not source:
            return []

        if i < len(path) - 1:
            if isinstance(source, list):
                source = source[0]
            elif isinstance(source, str):
                return []

    return source


def _get_references_from_expressions(resource: Dict, path: List[str]) -> List[str]:
    source = _get_value_from_expressions(resource, path)
    if not source or isinstance(source, str):
        return []

    return _get_referenced_resources(source)


""" Functions to extract information from the TFPLAN """


def security_groups_ids_from_network_interfaces(resource: {}) -> List[str]:
    return _get_references_from_expressions(resource, [
        'network_interfaces',
        'security_groups',
        'references',
    ])


def security_groups_ids_from_ingress_property(resource: {}) -> List[str]:
    return _get_references_from_expressions(resource, ['ingress', 'references'])


def security_groups_ids_from_egress_property(resource: {}) -> List[str]:
    return _get_references_from_expressions(resource, ['egress', 'references'])


def source_security_group_id_from_rule(resource: {}) -> str:
    sources_list = _get_references_from_expressions(resource, ['source_security_group_id', 'references'])
    if sources_list:
        return sources_list[0]


def security_group_id_from_rule(resource: {}) -> str:
    sg_ids = _get_references_from_expressions(resource, ['security_group_id', 'references'])
    if sg_ids:
        return sg_ids[0]


def security_group_rule_type(resource: {}) -> str:
    return _get_value_from_expressions(resource, ['type', 'constant_value'])
