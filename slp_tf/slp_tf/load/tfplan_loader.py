import json
from json import JSONDecodeError

from slp_tf.slp_tf.parse.mapping.mappers.tf_base_mapper import generate_resource_identifier
from sl_util.sl_util.json_utils import yaml_reader

from slp_base import ProviderLoader, LoadingIacFileError


def __read_source_files(sources: [bytes]):
    tf_config_present = False
    tf_plan_present = False

    for source in sources:
        try:
            json.loads(source)

            if tf_plan_present:
                raise LoadingIacFileError(
                    title='Multiple Terraform plan files',
                    message='Multiple Terraform plan files cannot be loaded at the same time.'
                )

            tf_plan_present = True
        except JSONDecodeError:
            tf_config_present = True

    return tf_config_present, tf_plan_present


def is_tfplan(sources: [bytes]) -> bool:
    tf_config_present, tf_plan_present = __read_source_files(sources)

    if tf_plan_present and not tf_config_present:
        return True

    if tf_config_present and not tf_plan_present:
        return False

    if tf_plan_present and tf_config_present:
        raise LoadingIacFileError(
            title='Mixed Terraform files',
            message='Terraform Config and Plan files cannot be loaded at the same time.'
        )


def map_modules(modules: [{}], parent: str = None) -> [{}]:
    resources = []

    for module in modules:
        module_address = get_module_address(module, parent)

        if 'resources' in module:
            resources.extend(map_resources(module['resources'], module_address))

        if 'child_modules' in module:
            resources.extend(map_modules(module['child_modules'], module_address))

    return resources


def map_resources(resources: [{}], parent: str = None) -> [{}]:
    mapped_resources = []
    for resource in resources:
        res_type = resource['type']
        res_name = get_resource_name(resource, parent)
        res_id = generate_resource_identifier(res_type, res_name)
        res_properties = map_resource_properties(resource)

        mapped_resource = {
            'resource_id': res_id,
            'resource_name': res_name,
            'resource_type': res_type,
            'resource_properties': res_properties
        }

        mapped_resource = apply_resource_retro_compatibility(mapped_resource)

        mapped_resources.append(mapped_resource)

    return mapped_resources


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
        **resource['values'],
        **resource['sensitive_values']
    }


def get_resource_name(resource: {}, parent: str) -> str:
    resource_base_name = resource['name'] if not parent else f'{parent}.{resource["name"]}'
    return f'{resource_base_name}_{resource["index"]}' if 'index' in resource else resource_base_name


def get_module_address(module: {}, parent: str) -> str:
    if 'address' in module:
        return f'{parent}.{module["address"]}' if parent else module['address']


class TfplanLoader(ProviderLoader):

    def __init__(self, source):
        self.source: bytes = source

        self.tfplan: dict = {}

        self.terraform: dict = {}

    def load(self):
        try:
            self.tfplan = yaml_reader(self.source)
            if self.tfplan:
                self.__map_tfplan_to_resources()
        except Exception:
            raise LoadingIacFileError(
                title='IaC file is not valid',
                message='The provided IaC file could not be processed'
            )

    def get_terraform(self):
        return self.terraform

    def __map_tfplan_to_resources(self):
        resources = map_modules([self.tfplan['planned_values']['root_module']])

        if resources:
            self.terraform = {'resource': resources}
