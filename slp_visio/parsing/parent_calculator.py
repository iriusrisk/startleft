from slp_visio.objects.diagram_objects import DiagramComponent, DiagramComponentOrigin


def calculate_area(component: DiagramComponent) -> float:
    return component.representation.area


def select_parent_by_area(parent_candidates: [DiagramComponent]) -> DiagramComponent:
    parent_candidates.sort(key=calculate_area)
    return parent_candidates[0]


def select_parent_by_centroid(child: DiagramComponent, parent_candidates: [DiagramComponent]) -> DiagramComponent:
    child_centroid = child.representation.centroid

    parent = None
    closest_distance = 0
    for parent_candidate in parent_candidates:
        distance = abs(parent_candidate.representation.centroid.distance(child_centroid))
        if parent is None or distance < closest_distance:
            parent = parent_candidate
            closest_distance = distance

    return parent


def select_parent(child: DiagramComponent, potential_parents: [DiagramComponent]) -> DiagramComponent:
    if len(potential_parents) == 1:
        return potential_parents[0]

    component_parents = list(filter(lambda p: p.origin == DiagramComponentOrigin.SIMPLE_COMPONENT,  potential_parents))
    if component_parents:
        return select_parent_by_area(component_parents)
    else:
        return select_parent_by_centroid(child, potential_parents)


def is_contained(parent_candidate: DiagramComponent, child_candidate: DiagramComponent) -> bool:
    return parent_candidate.id != child_candidate.id and \
           parent_candidate.representation.contains(child_candidate.representation)


class ParentCalculator:
    def __init__(self, component: DiagramComponent):
        self.child_candidate = component

    def calculate_parent(self, parent_candidates: [DiagramComponent]) -> DiagramComponent:
        potential_parents = []
        for parent_candidate in parent_candidates:
            if is_contained(parent_candidate, self.child_candidate):
                potential_parents.append(parent_candidate)

        if len(potential_parents) == 1:
            return potential_parents[0]

        if len(potential_parents) > 1:
            return select_parent_by_area(potential_parents)
