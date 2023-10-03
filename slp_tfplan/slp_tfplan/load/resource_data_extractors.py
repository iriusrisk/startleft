from typing import List, Dict, Literal


# TODO Consider migrating these functions to use jmespath


def _get_referenced_resources(references: List[str]):
    valid_references = []

    for reference in references:
        if reference.split('.')[-1] != 'id':
            valid_references.append(reference)

    return valid_references


def _get_value_from_path(source: Dict, path: List[str]):
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


def _get_from_values(resource: Dict, path: List[str]):
    expressions_path = ['resource_values'] + path
    return _get_value_from_path(resource, expressions_path)


def _get_from_expressions(resource: Dict, path: List[str]):
    expressions_path = ['resource_configuration', 'expressions'] + path
    return _get_value_from_path(resource, expressions_path)


def _get_references_from_expressions(resource: Dict, path: List[str]) -> List[str]:
    source = _get_from_expressions(resource, path)
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


def security_groups_ids_from_type_property(resource: {}, cidr_type: Literal['ingress', 'egress']) -> List[str]:
    return _get_references_from_expressions(resource, [cidr_type, 'references'])


def source_security_group_id_from_rule(resource: {}) -> str:
    sources_list = _get_references_from_expressions(resource, ['source_security_group_id', 'references'])
    if sources_list:
        return sources_list[0]


def security_group_id_from_rule(resource: {}) -> str:
    sg_ids = _get_references_from_expressions(resource, ['security_group_id', 'references'])
    if sg_ids:
        return sg_ids[0]


def cidr_from_type_property(resource: {}, cidr_type: Literal['ingress', 'egress']) -> List[dict]:
    return _get_from_values(resource, [cidr_type])


def description_from_rule(resource: {}) -> str:
    return _get_from_values(resource, ['description'])


def protocol_from_rule(resource: {}) -> str:
    return _get_from_values(resource, ['protocol'])


def from_port_from_rule(resource: {}) -> str:
    return _get_from_values(resource, ['from_port'])


def to_port_from_rule(resource: {}) -> str:
    return _get_from_values(resource, ['to_port'])


def cidr_blocks_from_rule(resource: {}) -> List[str]:
    return _get_from_values(resource, ['cidr_blocks'])


def security_group_rule_type(resource: {}) -> str:
    return _get_from_values(resource, ['type'])
