import re
from typing import Dict


def apply_resource_retro_compatibility(resource: {}):
    resource['_key'] = resource['resource_name']
    resource['Type'] = resource['resource_type']
    resource['Properties'] = resource['resource_properties']
    resource[resource['resource_type']] = {resource['resource_name']: resource['resource_properties']}
    # The order of the resource items matter for further processes
    return dict(reversed(resource.items()))


def map_resource_properties(resource: {}) -> {}:
    return {
        'resource_mode': resource['mode'],
        'resource_provider_name': resource['provider_name'],
        'resource_schema_version': resource['schema_version'],
        'resource_address': resource['address'],
        # Sensitive and usual values may be overlapped
        **resource.get('sensitive_values', {}),
        **resource.get('values', {})
    }


def is_resource_duplicated(resource: {}) -> bool:
    return 'index' in resource and not (resource['index'] == '0' or resource['index'] == 'zero')


def get_resource_id(resource: {}) -> str:
    return parse_address(resource['address']) \
        if 'index' in resource \
        else resource['address']


def get_resource_name(resource: {}, parent: str) -> str:
    return resource['name'] if not parent else f'{parent}.{resource["name"]}'


def get_module_address(module: {}, parent: str) -> str:
    if 'address' in module:
        module_address = parse_address(module['address'])
        return f'{parent}.{module_address}' if parent else module_address


def parse_address(address: str) -> str:
    return re.sub(r'\[.*?]', '', address)


class TfplanToResourceDict:
    def __init__(self, resources_configuration: Dict):
        self.resources_configuration = resources_configuration

    def map_modules(self, modules: [{}], parent: str = None) -> [{}]:
        mapped_modules = []
        resources = []

        for module in modules:
            module_address = get_module_address(module, parent)
            if module_address in mapped_modules:
                continue

            if 'resources' in module:
                resources.extend(self.__map_resources(module['resources'], module_address))

            if 'child_modules' in module:
                resources.extend(self.map_modules(module['child_modules'], module_address))

            mapped_modules.append(module_address)

        return resources

    def __map_resources(self, resources: [{}], parent: str = None) -> [{}]:
        mapped_resources = []
        for resource in resources:
            if is_resource_duplicated(resource):
                continue

            mapped_resource = {
                'resource_id': get_resource_id(resource),
                'resource_name': get_resource_name(resource, parent),
                'resource_type': resource['type'],
                'resource_properties':
                    self.__get_resource_configuration(resource['address']) or map_resource_properties(resource)
            }

            mapped_resource = apply_resource_retro_compatibility(mapped_resource)

            mapped_resources.append(mapped_resource)

        return mapped_resources

    def __get_resource_configuration(self, resource_address: str) -> Dict:
        return next(filter(lambda r: r['address'] == resource_address, self.resources_configuration), None)
