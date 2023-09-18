from typing import Union, List

from sl_util.sl_util import secure_regex
from sl_util.sl_util.iterations_utils import remove_keys
from slp_visio.slp_visio.load.objects.diagram_objects import DiagramComponent, Diagram
from slp_visio.slp_visio.load.visio_mapping_loader import VisioMappingFileLoader
from slp_visio.slp_visio.parse.visio_parser import VisioParser
from slp_visio.slp_visio.util.visio import normalize_label

AWS_REGEX = [r".*2017$", r".*AWS19$", r".*AWS2021$"]
AZURE_REGEX = [r"^AC.*Block$", r"^AE.*Block$", r"^AGS.*Block$", r"^AVM.*Block$", r".*Azure2019$", r".*Azure2021$"]
LUCID_CATCH_ALL_REGEX = AWS_REGEX + AZURE_REGEX


def _get_diagram_component_mapping_by_catch_all(resource: DiagramComponent, catch_all_config: [str]) \
        -> Union[None, dict]:
    for regex in LUCID_CATCH_ALL_REGEX:
        if secure_regex.match(regex, resource.type):
            return {'label': resource.type, 'type': catch_all_config}


class LucidParser(VisioParser):

    def __init__(self, project_id: str, project_name: str, diagram: Diagram, mapping_loader: VisioMappingFileLoader):
        super().__init__(project_id, project_name, diagram, mapping_loader)

    def _get_component_mappings(self) -> [dict]:
        """
        Returns the component mappings.
        After the component mappings are determined, the catch all mappings is determined.
        :return:
        """
        component_mappings: dict = super()._get_component_mappings()
        tz_mapped: dict = super()._get_trustzone_mappings()
        mapped_ids = list(tz_mapped.keys()) + list(component_mappings.keys())
        catch_all_components = self.__get_catch_all_mappings(ids_to_skip=mapped_ids)

        pruned_component_mappings = self.__prune_skip_components(component_mappings)
        pruned_catch_all_components = self.__prune_skip_components(catch_all_components)

        return {**pruned_catch_all_components, **pruned_component_mappings}

    def __get_catch_all_mappings(self, ids_to_skip) -> [dict]:
        result = {}
        catch_all_config = self.__get_catch_all_config()
        if not catch_all_config:
            return result
        for diag_component in self.diagram.components:
            if diag_component.id in ids_to_skip:
                continue
            mapping = _get_diagram_component_mapping_by_catch_all(diag_component, catch_all_config)
            if mapping:
                result[diag_component.id] = mapping
        return result

    def __get_catch_all_config(self):
        catch_all = self.mapping_loader.configuration.get('catch_all', False)
        if not catch_all or catch_all.lower() == 'false':
            return

        return catch_all.strip()

    def __get_skip_config(self) -> List[str]:
        return self.mapping_loader.configuration.get('skip')

    def __prune_skip_components(self, mappings):
        skip_config = self.__get_skip_config()
        if skip_config:
            skip_config_normalized = [normalize_label(s) for s in skip_config]
            ids_to_skip = {key for key, value in mappings.items()
                           if normalize_label(value.get('label')) in skip_config_normalized}
            return remove_keys(mappings, ids_to_skip)
        return mappings
