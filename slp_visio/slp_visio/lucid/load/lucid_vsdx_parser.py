from vsdx import Shape

from slp_visio.slp_visio.load.boundary_identifier import BoundaryIdentifier
from slp_visio.slp_visio.load.component_identifier import ComponentIdentifier
from slp_visio.slp_visio.load.parent_calculator import ParentCalculator
from slp_visio.slp_visio.load.vsdx_parser import VsdxParser


class LucidVsdxParser(VsdxParser):

    def _add_connector(self, connector_shape: Shape):
        shape_components = [c for c in self.page.child_shapes if ComponentIdentifier.is_component(c)
                            and not BoundaryIdentifier.is_boundary(c)]

        visio_connector = self.connector_factory.create_connector(connector_shape, shape_components)
        if visio_connector:
            self._visio_connectors.append(visio_connector)

    def _calculate_parents(self):
        trustzones_and_components = [c for c in self._visio_components if c.type != 'Line']
        for component in trustzones_and_components:
            component.parent = ParentCalculator(component).calculate_parent(trustzones_and_components)
