from sl_util.sl_util.iterations_utils import remove_from_list
from slp_visio.slp_visio.load.objects.diagram_objects import Diagram, DiagramComponent
from slp_visio.slp_visio.util.visio import normalize_label


class DiagramPruner:

    def __init__(self, diagram: Diagram, mapped_labels: [str]):
        self.components = diagram.components
        self.connectors = diagram.connectors
        self.normalized_mapped_labels = [normalize_label(mapped_label) for mapped_label in mapped_labels]

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
        map_by_name = normalize_label(component.name) in self.normalized_mapped_labels
        map_by_type = normalize_label(component.type) in self.normalized_mapped_labels

        return map_by_name or map_by_type

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
