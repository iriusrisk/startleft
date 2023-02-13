from typing import Callable

import pygraphviz
from networkx import nx_agraph
import json

from slp_tf.slp_tf.load.tf_loader import hcl2_reader
from sl_util.sl_util.file_utils import read_byte_data
from sl_util.sl_util.json_utils import yaml_reader

from slp_base import ProviderLoader, LoadingIacFileError


def __is_json(source: bytes):
    try:
        json.loads(source)
        return True
    except Exception:
        return False


def __is_graph(source: bytes):
    try:
        load_tfgraph(source)
        return True
    except Exception:
        return False


def __is_hcl2(source: bytes):
    try:
        hcl2_reader(source)
        return True
    except Exception:
        return False


def __get_source(sources: [bytes], selector: Callable) -> bytes:
    if len(sources) == 1 and selector(sources[0]):
        return sources[0]

    if len(sources) == 2:
        first_source_is_requested_type = selector(sources[0])
        second_source_is_requested_type = selector(sources[1])

        if first_source_is_requested_type and second_source_is_requested_type:
            raise LoadingIacFileError(
                title='Multiple Terraform plan files',
                message='Only one Terraform plan and an optional Terraform graph supported')

        if (first_source_is_requested_type and __is_hcl2(sources[1])) or \
                (second_source_is_requested_type and __is_hcl2(sources[0])):
            raise LoadingIacFileError(
                title='Mixed Terraform sources',
                message='Terraform config files mixed with Terraform plan or graph are not supported')

        if first_source_is_requested_type:
            return sources[0]
        if second_source_is_requested_type:
            return sources[1]


def get_tfplan(sources: [bytes]) -> bytes:
    return __get_source(sources, __is_json)


def get_tfgraph(sources: [bytes]) -> bytes:
    return __get_source(sources, __is_graph)


def load_tfgraph(source: bytes):
    return nx_agraph.from_agraph(pygraphviz.AGraph(read_byte_data(source)))


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
        if is_resource_duplicated(resource):
            continue

        mapped_resource = {
            'resource_id': get_resource_id(resource),
            'resource_name': get_resource_name(resource, parent),
            'resource_type': resource['type'],
            'resource_properties': map_resource_properties(resource)
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
        # Sensitive and usual values may be overlapped
        **resource['sensitive_values'],
        **resource['values']
    }


def is_resource_duplicated(resource: {}) -> bool:
    return 'index' in resource and not (resource['index'] == '0' or resource['index'] == 'zero')


def get_resource_id(resource: {}) -> str:
    return resource['address'].split('[')[0] \
        if 'index' in resource \
        else resource['address']


def get_resource_name(resource: {}, parent: str) -> str:
    return resource['name'] if not parent else f'{parent}.{resource["name"]}'


def get_module_address(module: {}, parent: str) -> str:
    if 'address' in module:
        return f'{parent}.{module["address"]}' if parent else module['address']


class TfplanLoader(ProviderLoader):

    def __init__(self, tfplan_source: bytes, tfgraph_source: bytes = None):
        self.tfplan_source: bytes = tfplan_source
        self.tfgraph_source: bytes = tfgraph_source

        self.tfplan: dict = {}

        self.terraform: dict = {}
        self.tfgraph: dict = {}

    def load(self):
        self.__load_tfplan()

        if self.tfgraph_source:
            self.tfgraph = load_tfgraph(self.tfgraph_source)

    def get_terraform(self):
        return self.terraform

    def get_tfgraph(self):
        return self.tfgraph

    def __load_tfplan(self):
        try:
            self.tfplan = yaml_reader(self.tfplan_source)
            if self.tfplan:
                self.__map_tfplan_to_resources()
        except Exception:
            raise LoadingIacFileError(
                title='IaC file is not valid',
                message='The provided IaC file could not be processed'
            )

    def __map_tfplan_to_resources(self):
        resources = map_modules([self.tfplan['planned_values']['root_module']])

        if resources:
            self.terraform = {'resource': resources}
