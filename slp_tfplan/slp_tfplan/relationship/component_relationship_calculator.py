from enum import Enum

from otm.otm.entity.parent_type import ParentType
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanComponent, TFPlanOTM
from slp_tfplan.slp_tfplan.util.tfplan import find_component_by_id


class ComponentRelationshipType(Enum):
    SAME = 1
    ANCESTOR = 2
    ANCESTOR_OF_ANY_CLONE = 3
    DESCENDANT = 4
    DESCENDANT_OF_ANY_CLONE = 5
    UNRELATED = 6


class ComponentRelationshipCalculator:
    """
    This class is used to calculate the relationship between two components inside an OTM.
    """

    def __init__(self, tfplan_otm: TFPlanOTM):
        self.tfplan_otm = tfplan_otm

    def get_relationship(self, component_from: TFPlanComponent, component_to: TFPlanComponent) \
            -> ComponentRelationshipType:
        """
        This method returns the relationship between two components.
        component_from is {ComponentRelationshipType} of component_to
        ej: ALB is DESCENDANT of VPC

        :param component_from: The component to get the relation from
        :param component_to: The component to get the relation to
        :return: The relationship type between from the component to the related component
        """
        if component_from.id == component_to.id:
            return ComponentRelationshipType.SAME
        elif self.__is_ancestor(component_to, component_from):
            return ComponentRelationshipType.ANCESTOR
        elif self.__is_ancestor(component_from, component_to):
            return ComponentRelationshipType.DESCENDANT
        elif self.__is_ancestor_of_any_clone(component_to, component_from):
            return ComponentRelationshipType.ANCESTOR_OF_ANY_CLONE
        elif self.__is_ancestor_of_any_clone(component_from, component_to):
            return ComponentRelationshipType.DESCENDANT_OF_ANY_CLONE

        return ComponentRelationshipType.UNRELATED

    def are_related(self, first: TFPlanComponent, second: TFPlanComponent) -> bool:
        """
        This method returns whether two components are related.
        :param first: The first component
        :param second: The second component
        :return: True if the two components are related, False otherwise
        """
        return self.get_relationship(first, second) != ComponentRelationshipType.UNRELATED

    def __is_ancestor(self, component: TFPlanComponent, ancestor: TFPlanComponent) -> bool:
        return component.parent_type == ParentType.COMPONENT and \
               (component.parent == ancestor.id
                or self.__is_ancestor(find_component_by_id(component.parent, self.tfplan_otm.components), ancestor))

    def __is_ancestor_of_any_clone(self, component: TFPlanComponent, ancestor: TFPlanComponent) -> bool:
        if not component.clones_ids:
            return False

        for clone_id in component.clones_ids:
            if self.__is_ancestor(find_component_by_id(clone_id, self.tfplan_otm.components), ancestor):
                return True

        return False
