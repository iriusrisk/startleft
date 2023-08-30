from typing import Dict, Tuple

from otm.otm.entity.representation import RepresentationElement


def make_relative(representation: RepresentationElement, parent_position: Dict[str, float]):
    representation.position = build_position(*_get_relative_position(representation.position['x'],
                                                                     representation.position['y'],
                                                                     parent_position['x'],
                                                                     parent_position['y']))


def build_position(left_x: float, top_y: float, padding: float = 0) -> Dict[str, float]:
    return {'x': left_x - padding, 'y': top_y - padding}


def build_size(left_x: float, right_x: float, top_y: float, bottom_y: float, padding: float = 0) -> Dict[str, float]:
    return {'width': (right_x - left_x) + (padding * 2), 'height': (bottom_y - top_y) + (padding * 2)}


def _get_relative_position(absolute_x: float, absolute_y: float, parent_x: float, parent_y: float) \
        -> Tuple[float, float]:
    return absolute_x - parent_x, absolute_y - parent_y
