from sl_util.sl_util.iterations_utils import remove_from_list
from slp_visio.slp_visio.load.objects.diagram_objects import Diagram, DiagramComponent


class DiagramPruner:

    def __init__(self, diagram: Diagram, shape_ids_mapped: [str]):
        self.components = diagram.components
        self.connectors = diagram.connectors
        self.shape_ids_mapped = shape_ids_mapped

        self.__removed_components = []

    def run(self):
        self.__remove_unmapped_components()

        self.__prune_orphan_connectors()
        self.__restore_parents()

    def __remove_unmapped_components(self):
        remove_from_list(
            self.components,
            lambda component: not self.__is_component_mapped(component),
            self.__remove_component
        )

    def __prune_orphan_connectors(self):
        removed_components_ids = [removed_component.id for removed_component in self.__removed_components]
        remove_from_list(
            self.connectors,
            lambda connector: connector.from_id in removed_components_ids or connector.to_id in removed_components_ids
        )

    def __restore_parents(self):
        self.__squash_removed_components()

        removed_parents = dict(zip(
            [dc.id for dc in self.__removed_components], [dc.parent for dc in self.__removed_components]))

        for diagram_component in self.components:
            if diagram_component.parent and diagram_component.parent.id in removed_parents:
                diagram_component.parent = removed_parents[diagram_component.parent.id]

    def __is_component_mapped(self, component: DiagramComponent):
        return component.id in self.shape_ids_mapped

    def __remove_component(self, component: DiagramComponent):
        self.components.remove(component)
        self.__store_removed_component(component)

    def __store_removed_component(self, component: DiagramComponent):
        self.__removed_components.append(component)

    def __squash_removed_components(self):
        for removed_component in self.__removed_components:
            removed_component.parent = self.__find_alive_parent(removed_component)

    def __find_alive_parent(self, component: DiagramComponent):
        if component.parent is None:
            return None

        if component.parent not in self.__removed_components:
            return component.parent

        self.__find_alive_parent(component.parent)
