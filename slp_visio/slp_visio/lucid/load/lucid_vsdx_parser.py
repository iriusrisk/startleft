from vsdx import Shape

from slp_visio.slp_visio.load.parent_calculator import ParentCalculator
from slp_visio.slp_visio.load.vsdx_parser import VsdxParser

LUCID_LINE = 'com.lucidchart.Line'


class LucidVsdxParser(VsdxParser):

    @staticmethod
    def _is_connector(shape: Shape) -> bool:
        for connect in shape.connects:
            if shape.ID == connect.connector_shape_id:
                return True

        if shape.shape_name and shape.shape_name.startswith(f'{LUCID_LINE}'):
            return True

        return False

    def _add_connector(self, connector_shape: Shape):
        shape_components = [c for c in self.page.child_shapes if self._is_component(c) and not self._is_boundary(c)]

        visio_connector = self.connector_factory.create_connector(connector_shape, shape_components)
        if visio_connector:
            self._visio_connectors.append(visio_connector)

    def _calculate_parents(self):
        trustzones_and_components = [c for c in self._visio_components if c.type != 'Line']
        for component in trustzones_and_components:
            component.parent = ParentCalculator(component).calculate_parent(trustzones_and_components)
