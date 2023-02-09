from typing import Optional

from otm.otm.entity.component import Component


def is_trustzone_parent(component: Component):
    return component.parent_type == 'trustZone'


class TerraformPathIdsCalculator:

    def __init__(self, components: [Component], id_generator):
        self.components = components
        self.id_generator = id_generator

        self.path_ids = {}

    def calculate_path_ids(self) -> {}:
        for component in self.components:
            if component.id not in self.path_ids:
                self.__calculate_path_id(component)

        return self.path_ids

    def __calculate_path_id(self, component: Component) -> Optional[str]:
        parent_path_id = self.__get_parent_path_id(component)
        if not parent_path_id:
            return None

        path_id = self.__generate_component_id(component, parent_path_id)

        self.path_ids[component.id] = path_id

        return path_id

    def __get_parent_path_id(self, component: Component) -> Optional[str]:
        if is_trustzone_parent(component):
            return component.parent

        if component.parent in self.path_ids:
            return self.path_ids[component.parent]

        parent_component = self.__find_parent_component(component.parent)
        if not parent_component:
            return None

        return self.__calculate_path_id(parent_component)

    def __find_parent_component(self, parent_id: str):
        return next(filter(lambda x: x.id == parent_id, self.components), None)

    def __generate_component_id(self, component: Component, parent_id: str):
        return self.id_generator.from_component_source(component.source, parent_id, component.name).generate_id()
