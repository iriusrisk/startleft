from sl_util.sl_util.secure_regex import SecureRegexWrapper as re
from typing import Dict, List


def map_resource_properties(resource: Dict) -> {}:
    return {
        'resource_mode': resource['mode'],
        'resource_provider_name': resource['provider_name'],
        'resource_schema_version': resource['schema_version'],
        'resource_address': resource['address'],
        # Sensitive and usual values may be overlapped
        **resource.get('sensitive_values', {}),
        **resource.get('values', {})
    }


def is_not_cloned_resource(resource: Dict) -> bool:
    return 'index' not in resource or resource['index'] == '0' or resource['index'] == 'zero'


def get_resource_id(resource: Dict) -> str:
    return parse_address(resource['address']) \
        if 'index' in resource \
        else resource['address']


def get_resource_name(resource: Dict, parent: str) -> str:
    return resource['name'] if not parent else f'{parent}.{resource["name"]}'


def get_module_address(module: Dict, parent: str) -> str:
    if 'address' in module:
        module_address = parse_address(module['address'])
        return f'{parent}.{module_address}' if parent else module_address


def parse_address(address: str) -> str:
    return remove_name_prefix(remove_index(address)) if address else None


def remove_index(address: str) -> str:
    return re.sub(r'\[.*?]', '', address)


def remove_name_prefix(address: str) -> str:
    return re.sub(r'(.*)_name_prefix$', r'\1', address) if address else None


class TfplanToResourceDict:
    def __init__(self, resources_configuration: Dict):
        self.resources_configuration = resources_configuration

    def map_modules(self, modules: List[Dict], parent: str = None) -> List[Dict]:
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

    def __map_resources(self, resources: List[Dict], parent: str = None) -> List[Dict]:
        return list(map(lambda r: self.__map_resource(r, parent), filter(is_not_cloned_resource, resources)))

    def __map_resource(self, resource: Dict, parent: str = None) -> Dict:
        return {
            'resource_id': get_resource_id(resource),
            'resource_name': get_resource_name(resource, parent),
            'resource_type': resource['type'],
            'resource_properties':
                self.__get_resource_configuration(resource['address']) or map_resource_properties(resource)
        }

    def __get_resource_configuration(self, resource_address: str) -> Dict:
        return next(filter(lambda r: r['address'] == resource_address, self.resources_configuration), None)
