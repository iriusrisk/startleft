from startleft.diagram.visio_objects import VisioComponent


def calculate_area(component: VisioComponent) -> float:
    return component.representation.area


def select_parent_by_area(parent_candidates: [VisioComponent]) -> VisioComponent:
    parent_candidates.sort(key=calculate_area)
    return parent_candidates[0]


def is_contained(parent_candidate: VisioComponent, child_candidate: VisioComponent) -> bool:
    return parent_candidate.id != child_candidate.id and \
           parent_candidate.representation.contains(child_candidate.representation)


class ParentCalculator:
    child_candidate: VisioComponent

    def __init__(self, visio_component: VisioComponent):
        self.child_candidate = visio_component

    def calculate_parent(self, parent_candidates: [VisioComponent]) -> VisioComponent:
        potential_parents = []
        for parent_candidate in parent_candidates:
            if is_contained(parent_candidate, self.child_candidate):
                potential_parents.append(parent_candidate)

        if len(potential_parents) == 1:
            return potential_parents[0]

        if len(potential_parents) > 1:
            return select_parent_by_area(potential_parents)
