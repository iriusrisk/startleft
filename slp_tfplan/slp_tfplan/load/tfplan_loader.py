from typing import List, Dict, Union

import pygraphviz
from networkx import nx_agraph, DiGraph

from sl_util.sl_util.json_utils import yaml_reader
from sl_util.sl_util.file_utils import read_byte_data

from slp_base import ProviderLoader, LoadingIacFileError
from slp_tfplan.slp_tfplan.load.tfplan_to_resource_dict import TfplanToResourceDict


def load_tfplan(source: bytes) -> Dict:
    try:
        return yaml_reader(source)
    except Exception:
        pass


def load_tfgraph(source: bytes) -> DiGraph:
    try:
        return nx_agraph.from_agraph(pygraphviz.AGraph(read_byte_data(source)))
    except Exception:
        pass


def generate_invalid_iac_files_error() -> LoadingIacFileError:
    return LoadingIacFileError(
        title='IaC files are not valid',
        message='The provided IaC files could not be processed'
    )


def generate_wrong_number_of_sources_error() -> LoadingIacFileError:
    return LoadingIacFileError(
        title='Wrong number of files',
        message='Required one tfplan and one tfgraph files'
    )


class TfplanLoader(ProviderLoader):

    def __init__(self, sources: List[bytes]):
        self.sources = sources

        self.tfplan: Union[Dict, None] = None
        self.tfgraph: Union[Dict, None] = None

        self.terraform: dict = {}

    def load(self):
        self.__load_sources()
        if self.tfplan:
            self.__map_tfplan_to_resources()

    def get_terraform(self):
        return self.terraform

    def get_tfgraph(self):
        return self.tfgraph

    def __load_sources(self):
        if len(self.sources) != 2:
            raise generate_wrong_number_of_sources_error()

        for source in self.sources:
            if self.tfplan is None:
                self.tfplan = load_tfplan(source)
                if self.tfplan is not None:
                    continue

            if self.tfgraph is not None:
                raise generate_invalid_iac_files_error()

            self.tfgraph = load_tfgraph(source)

            if self.tfgraph is None:
                raise generate_invalid_iac_files_error()

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
