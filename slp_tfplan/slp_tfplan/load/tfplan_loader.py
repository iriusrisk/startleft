from typing import Callable, List, Dict

import pygraphviz
from networkx import nx_agraph

from sl_util.sl_util.file_utils import read_byte_data
from sl_util.sl_util.json_utils import yaml_reader, is_json

from slp_base import ProviderLoader, LoadingIacFileError
from slp_tfplan.slp_tfplan.load.tfplan_to_resource_dict import TfplanToResourceDict


def __is_graph(source: bytes):
    try:
        load_tfgraph(source)
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

        if first_source_is_requested_type:
            return sources[0]
        if second_source_is_requested_type:
            return sources[1]


def get_tfplan(sources: [bytes]) -> bytes:
    return __get_source(sources, is_json)


def get_tfgraph(sources: [bytes]) -> bytes:
    return __get_source(sources, __is_graph)


def load_tfgraph(source: bytes):
    return nx_agraph.from_agraph(pygraphviz.AGraph(read_byte_data(source)))


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
        resources = TfplanToResourceDict(self.__get_tfplan_resources()).map_modules(self.__get_tfplan_root_module())

        if resources:
            self.terraform = {'resource': resources}

    def __get_tfplan_resources(self) -> Dict:
        return self.tfplan \
            .get('configuration', {}) \
            .get('root_module', {}) \
            .get('resources', {})

    def __get_tfplan_root_module(self) -> List[Dict]:
        return [self.tfplan['planned_values']['root_module']]