from startleft.diagram.objects.diagram_objects import Diagram, DiagramComponent


class DiagramPruner:

    def __init__(self, diagram: Diagram, mapped_labels: [str]):
        self.components = diagram.components
        self.connectors = diagram.connectors
        self.mapped_labels = mapped_labels

        self.removed_components = []

    def run(self):
        self.__remove_unmapped_components()
        self.__prune_orphan_connectors()
        self.__restore_parents()

    def __prune_orphan_connectors(self):
        removed_components_ids = [removed_component.id for removed_component in self.removed_components]
        for diagram_connector in self.connectors:
            if diagram_connector.from_id in removed_components_ids \
                    or diagram_connector.to_id in removed_components_ids:
                self.connectors.remove(diagram_connector)

    def __restore_parents(self):
        self.__squash_removed_components()

        removed_parents = dict(zip(
            [dc.id for dc in self.removed_components], [dc.parent for dc in self.removed_components]))

        for diagram_component in self.components:
            if diagram_component.parent and diagram_component.parent.id in removed_parents:
                diagram_component.parent = removed_parents[diagram_component.parent.id]

    def __remove_unmapped_components(self):
        # This weird while needs to be done because:
        # - The foreach does not work if you remove an element from the list
        # - The remove has to be invoked on the list to affect the object passed as a class attribute
        i = 0
        while i < len(self.components):
            if not self.__is_component_mapped(self.components[i]):
                self.__remove_component(self.components[i])
            else:
                i = i + 1

        for component in self.components:
            if not self.__is_component_mapped(component):
                self.__remove_component(component)

    def __is_component_mapped(self, component: DiagramComponent):
        return component.name in self.mapped_labels or component.type in self.mapped_labels

    def __remove_component(self, component: DiagramComponent):
        self.components.remove(component)
        self.__store_removed_component(component)

    def __store_removed_component(self, component: DiagramComponent):
        self.removed_components.append(component)

    def __squash_removed_components(self):
        for removed_component in self.removed_components:
            removed_component.parent = self.__find_alive_parent(removed_component)

    def __find_alive_parent(self, component: DiagramComponent):
        if component.parent is None:
            return None

        if component.parent not in self.removed_components:
            return component.parent

        self.__find_alive_parent(component.parent)
