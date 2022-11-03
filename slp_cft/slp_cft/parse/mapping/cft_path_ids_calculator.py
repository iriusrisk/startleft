from otm.otm.otm import Component
from slp_cft.slp_cft.parse.mapping.cft_component_id_generator import CloudformationComponentIdGenerator


class CloudformationPathIdsCalculator:

    def __init__(self, components: [Component]):
        self.components = components

        self.path_ids = {}

    def calculate_path_ids(self) -> {}:
        for component in self.components:
            if component.id not in self.path_ids:
                self.__calculate_path_id(component)

        return self.path_ids

    def __calculate_path_id(self, component: {}) -> str:
        path_id = self.__build_component_id(component, self.__get_parent_path_id(component))

        self.path_ids[component.id] = path_id

        return path_id

    def __get_parent_path_id(self, component: Component) -> str:
        if component.parent_type == 'trustZone':
            return component.parent

        if component.parent in self.path_ids:
            return self.path_ids[component.parent]

        return self.__calculate_path_id(self.__find_parent_component(component.parent))

    def __find_parent_component(self, parent_id: str):
        return next(filter(lambda x: x.id == parent_id, self.components), None)

    def __build_component_id(self, component: {}, parent_id: str):
        return CloudformationComponentIdGenerator.from_component(component.source, parent_id).generate_id()
