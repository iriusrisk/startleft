from typing import List

from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanComponent


def find_component_by_id(component_id: str, components: List[TFPlanComponent]) -> TFPlanComponent:
    """
    Returns the component with the given id.
    :param component_id: The id of the component to find.
    :param components: The list of components to search in.
    :return:
    """
    return next(filter(lambda c: c.id == component_id, components))
