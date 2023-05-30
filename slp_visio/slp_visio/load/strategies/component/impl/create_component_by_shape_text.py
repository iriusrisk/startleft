from typing import Optional

from vsdx import Shape

from slp_visio.slp_visio.load.objects.diagram_objects import DiagramComponent
from slp_visio.slp_visio.load.representation.visio_shape_representer import VisioShapeRepresenter
from slp_visio.slp_visio.load.strategies.component.create_component_strategy import CreateComponentStrategy
from slp_visio.slp_visio.util.visio import get_shape_text, get_master_shape_text, normalize_label, get_unique_id_text

LUCID_COMPONENT_PREFIX = 'com.lucidchart'


class CreateComponentByShapeText(CreateComponentStrategy):
    """
    Strategy to create a component from the shape text
    """

    def create_component(self, shape: Shape, origin=None, representer: VisioShapeRepresenter = None) \
            -> Optional[DiagramComponent]:
        name = get_shape_text(shape)
        if name:
            return DiagramComponent(
                id=shape.ID,
                name=normalize_label(name),
                type=normalize_label(self.get_component_type(shape)),
                origin=origin,
                representation=representer.build_representation(shape),
                unique_id=get_unique_id_text(shape))

    def get_component_type(self, shape):
        if self.is_lucid(shape):
            return self.get_lucid_component_type(shape)
        else:
            return get_master_shape_text(shape)

    @staticmethod
    def is_lucid(shape: Shape):
        return shape.shape_name and shape.shape_name.startswith(LUCID_COMPONENT_PREFIX)

    @staticmethod
    def get_lucid_component_type(shape: Shape):
        return shape.shape_name.replace(f'{LUCID_COMPONENT_PREFIX}.', '').replace(f'.{shape.ID}', '')
