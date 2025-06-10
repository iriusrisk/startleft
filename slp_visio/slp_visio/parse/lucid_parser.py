from typing import Optional

from sl_util.sl_util.iterations_utils import remove_keys
from slp_visio.slp_visio.load.objects.diagram_objects import Diagram
from slp_visio.slp_visio.load.visio_mapping_loader import VisioMappingFileLoader
from slp_visio.slp_visio.parse.visio_parser import VisioParser, _match_resource

class LucidParser(VisioParser):

    def __init__(self, project_id: str, project_name: str, diagram: Diagram, mapping_loader: VisioMappingFileLoader):
        super().__init__(project_id, project_name, diagram, mapping_loader)

    def _get_component_mappings(self) -> dict:
        """
        Returns the component mappings.
        After the component mappings are determined, the catch all mappings is determined.
        :return:
        """
        component_mappings: dict = super()._get_component_mappings()
        tz_mapped: dict = super()._get_trustzone_mappings()
        mapped_ids = list(tz_mapped.keys()) + list(component_mappings.keys())
        catch_all_components = self.__get_catch_all_mappings(ids_to_skip=mapped_ids)

        return self.__prune_skip_components({**catch_all_components, **component_mappings})

    def __get_catch_all_mappings(self, ids_to_skip) -> dict:
        catch_all_type = self.__get_catch_all_type()
        return {
            c.id: {'label': c.type, 'type': catch_all_type}
            for c in self.diagram.components
            if c.id not in ids_to_skip
        } if catch_all_type else {}

    def __get_catch_all_type(self) -> Optional[str]:
        catch_all = self.mapping_loader.configuration.get('catch_all')
        return catch_all.strip() if catch_all and catch_all.lower() != 'false' else None

    def __prune_skip_components(self, mappings: dict) -> dict:
        return remove_keys(mappings, self.__get_ids_to_skip())

    def __get_ids_to_skip(self) -> list[str]:
        skip_config = self.__get_skip_config()
        return [
            component.id
            for component in self.diagram.components
            for skip in skip_config
            if _match_resource(component.type, skip)
        ] if skip_config else []

    def __get_skip_config(self) -> list[str]:
        return self.mapping_loader.configuration.get('skip')