from otm.otm.entity.representation import RepresentationElement
from slp_visio.slp_visio.load.objects.diagram_objects import DiagramLimits, DiagramComponent, DiagramComponentOrigin

# TODO: Make the scale of the output representations parametrizable
IRIUSRISK_SMALLEST_COMPONENT_SIZE = 82
VISIO_STENCILS_DEFAULT_SIZE = 0.5
SCALE_FACTOR: int = round(IRIUSRISK_SMALLEST_COMPONENT_SIZE / VISIO_STENCILS_DEFAULT_SIZE)


def scale_to_int(value: float) -> int:
    return round(value * SCALE_FACTOR)


def get_scaled_coordinates(component: DiagramComponent) -> ():
    minx, miny, maxx, maxy = component.representation.bounds
    return scale_to_int(minx), scale_to_int(maxy)


def has_representation(component: DiagramComponent) -> bool:
    if not component.representation or component.origin == DiagramComponentOrigin.BOUNDARY:
        return False

    if not component.trustzone and (not component.parent or not component.parent.representation):
        return False

    if component.parent and component.parent.origin == DiagramComponentOrigin.BOUNDARY:
        return False

    return True


def build_size_object(wh: ()) -> dict:
    return {'width': wh[0], 'height': wh[1]}


def calculate_diagram_size(diagram_limits: DiagramLimits) -> ():
    return scale_to_int(diagram_limits.x_top) - scale_to_int(diagram_limits.x_floor), \
           scale_to_int(diagram_limits.y_top) - scale_to_int(diagram_limits.y_floor)


def calculate_size(component: DiagramComponent) -> ():
    minx, miny, maxx, maxy = component.representation.bounds
    return scale_to_int(maxx) - scale_to_int(minx), scale_to_int(maxy) - scale_to_int(miny)


class RepresentationCalculator:

    def __init__(self, diagram_representation_id: str, limits: DiagramLimits):
        self.diagram_representation_id = diagram_representation_id
        self.limits = limits

    def calculate_representation(self, component: DiagramComponent):
        if not has_representation(component):
            return None

        return RepresentationElement(
            id_=f'{component.id}-representation',
            name=f'{component.name} Representation',
            representation=self.diagram_representation_id,
            position=self.__build_position(component),
            size=build_size_object(calculate_size(component))
        )

    def __build_position(self, component: DiagramComponent):
        xleft, ytop = self.__calculate_position(component)

        return {'x': xleft, 'y': ytop}

    def __calculate_position(self, component: DiagramComponent):
        xleft, ytop = get_scaled_coordinates(component)
        xmin, ymax = self.__get_parent_coordinates(component)

        return xleft - xmin, ymax - ytop

    def __get_parent_coordinates(self, component):
        return get_scaled_coordinates(component.parent) \
            if component.parent \
            else self.__get_diagram_origin()

    def __get_diagram_origin(self) -> ():
        return scale_to_int(self.limits.x_floor), scale_to_int(self.limits.y_top)
