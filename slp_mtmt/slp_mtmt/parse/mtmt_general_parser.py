from typing import Union

from slp_mtmt.slp_mtmt.entity.mtmt_entity_border import MTMBorder
from slp_mtmt.slp_mtmt.entity.mtmt_entity_line import MTMLine
from slp_mtmt.slp_mtmt.mtmt_entity import MTMT
from slp_mtmt.slp_mtmt.mtmt_mapping_file_loader import MTMTMapping
from slp_mtmt.slp_mtmt.util.border_parent_calculator import BorderParentCalculator
from slp_mtmt.slp_mtmt.util.line_parent_calculator import LineParentCalculator


def is_parent(parent, child):
    if isinstance(parent, MTMBorder):
        if BorderParentCalculator.is_parent(parent, child):
            return True
    elif isinstance(parent, MTMLine):
        if LineParentCalculator.is_parent(parent, child):
            return True
    return False


def get_the_child(parents) -> Union[MTMBorder, MTMLine, None]:
    if len(parents) == 0:
        return None
    if len(parents) == 1:
        return parents[0]
    candidate = parents[0]
    for parent in parents[1:]:
        new_child = which_is_child(candidate, parent)
        if new_child is not None:
            candidate = new_child
    return candidate


def which_is_child(one, two):
    if is_parent(one, two):
        return two
    elif is_parent(two, one):
        return one


class MTMTGeneralParser:

    def __init__(self, source: MTMT, mapping: MTMTMapping, diagram_representation: str):
        self.source = source
        self.mapping = mapping
        self.diagram_representation = diagram_representation

    def _get_parent(self, border: MTMBorder)  -> Union[MTMBorder, MTMLine, None]:
        parents = []
        for candidate in self.source.borders + self.source.lines:
            if is_parent(candidate, border):
                parents.append(candidate)
        return get_the_child(parents)
