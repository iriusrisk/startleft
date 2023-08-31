from typing import Union, List

from sl_util.sl_util import secure_regex
from slp_visio.slp_visio.load.objects.diagram_objects import DiagramComponent, Diagram
from slp_visio.slp_visio.load.visio_mapping_loader import VisioMappingFileLoader
from slp_visio.slp_visio.parse.visio_parser import VisioParser

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

    def __get_ids_to_skip(self) -> [str]:
        """
        Returns the ids of the components that are mapped as trustzones or as components.
        :return:
        """
        return list(super()._get_trustzone_mappings().keys()) + list(super()._get_component_mappings().keys())

    def _get_component_mappings(self) -> [dict]:
        """
        Returns the component mappings.
        After the component mappings are determined, the catch all mappings is determined.
        :return:
        """
        component_mappings = super()._get_component_mappings()
        catch_all_components = self.__get_catch_all_mappings(ids_to_skip=self.__get_ids_to_skip())

        component_mappings = self.__prune__skip__components(component_mappings)
        catch_all_components = self.__prune__skip__components(catch_all_components)

        return {**catch_all_components, **component_mappings}

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
    
    def __prune__skip__components(self, components):

        components_to_skip = self.__get_skip_config()
        if components_to_skip is not None:
            components = {key: value for key, value in components.items() if value.get('type') not in components_to_skip}
        return components
