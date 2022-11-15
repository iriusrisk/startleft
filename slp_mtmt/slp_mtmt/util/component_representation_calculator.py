from otm.otm.otm import RepresentationElement
from slp_mtmt.slp_mtmt.entity.mtmt_entity_border import MTMBorder


class ComponentRepresentationCalculator:

    @staticmethod
    def calculate_representation(border: MTMBorder, representation: str,
                                 parent: MTMBorder = None) -> RepresentationElement:
        representation_id = border.id + '-representation'
        representation_name = border.name + ' Representation'
        if parent:
            x, y = ComponentRepresentationCalculator.get_relative_coordinates(border, parent)
        else:
            x, y = border.left, border.top
        position = {"x": x, "y": y}
        size = {"width": border.width, "height": border.height}
        return RepresentationElement(id_=representation_id, name=representation_name,
                                     representation=representation, position=position, size=size)

    @staticmethod
    def get_relative_coordinates(border: MTMBorder, parent: MTMBorder) -> (int, int):
        x = border.left - parent.left
        y = border.top - parent.top
        return x, y
