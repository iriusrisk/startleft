from typing import Dict, List

import sl_util.sl_util.secure_regex as re
from sl_util.sl_util.str_utils import to_number


def is_not_cloned_resource(resource: Dict) -> bool:
    return to_number(resource['index']) == 0 if 'index' in resource else True


def get_resource_id(resource: Dict) -> str:
    return parse_address(resource['address']) if 'address' in resource else None


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
            'resource_values': resource.get('values', {}),
            'resource_configuration': {
                'expressions': self.__get_resource_configuration_expressions(resource)
            }
        }

    def __get_resource_configuration_expressions(self, resource: Dict) -> Dict:
        return self.__get_resource_configuration(resource).get('expressions', {})

    def __get_resource_configuration(self, resource: Dict) -> Dict:
        return next(filter(lambda r: r['address'] == resource['address'], self.resources_configuration), {})
