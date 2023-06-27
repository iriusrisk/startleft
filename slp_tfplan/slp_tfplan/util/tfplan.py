from typing import List, Dict, Union

from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanComponent


def __compare_unordered_list_or_string(a, b):
    if isinstance(a, str) and isinstance(b, str):
        return a == b
    elif isinstance(a, str) and isinstance(b, list):
        return sorted([a]) == sorted(b)
    elif isinstance(a, list) and isinstance(b, list):
        return sorted(a) == sorted(b)
    else:
        return False


def find_component_by_id(component_id: str, components: List[TFPlanComponent]) -> TFPlanComponent:
    """
    Returns the component with the given id.
    :param component_id: The id of the component to find.
    :param components: The list of components to search in.
    :return:
    """
    return next(filter(lambda c: c.id == component_id, components))


def find_variable_name_by_value(variables: Dict[str, Union[list, str]], value: Union[list, str]) -> str:
    """
    Returns the name of the variable that has the given value.
    :param variables:
    :param value:
    :return:
    """
    for k, v in variables.items():
        if __compare_unordered_list_or_string(v, value):
            return k
