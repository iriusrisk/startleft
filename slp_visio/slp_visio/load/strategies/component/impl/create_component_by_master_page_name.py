from typing import Optional

from vsdx import Shape

from sl_util.sl_util.injection import register
from slp_visio.slp_visio.load.objects.diagram_objects import DiagramComponent
from slp_visio.slp_visio.load.representation.visio_shape_representer import VisioShapeRepresenter
from slp_visio.slp_visio.load.strategies.component.create_component_strategy import CreateComponentStrategy, \
    CreateComponentStrategyContainer
from slp_visio.slp_visio.load.strategies.component.impl.component_identifier_by_master_page_name import \
    ComponentIdentifierByMasterPageName
from slp_visio.slp_visio.load.strategies.component.impl.create_component_by_shape_text import CreateComponentByShapeText
from slp_visio.slp_visio.util.visio import normalize_label, get_unique_id_text, get_shape_text


@register(CreateComponentStrategyContainer.visio_strategies)
class CreateComponentByMasterPageName(CreateComponentStrategy):
    """
    Strategy to create a component from the master shape name
    """

    def create_component(self, shape: Shape, origin=None, representer: VisioShapeRepresenter = None) \
            -> Optional[DiagramComponent]:
        if ComponentIdentifierByMasterPageName().get_master_page_name(shape):
            component_type = self.get_component_type(shape)
            name = get_shape_text(shape.child_shapes) or normalize_label(component_type)
            return DiagramComponent(
                id=shape.ID,
                name=normalize_label(name),
                type=component_type,
                origin=origin,
                representation=representer.build_representation(shape),
                unique_id=get_unique_id_text(shape))

    @staticmethod
    def get_component_type(shape):
        if CreateComponentByShapeText.is_lucid(shape):
            return CreateComponentByShapeText.get_lucid_component_type(shape)
        else:
            return ComponentIdentifierByMasterPageName().get_master_page_name(shape)
