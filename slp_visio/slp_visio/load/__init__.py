from .strategies.connector.impl import connector_identifier_by_connects, create_connector_by_connects, \
    create_connector_by_line_coordinates
from .strategies.component.impl import component_identifier_by_shape_text, create_component_by_shape_text, \
    component_identifier_by_master_page_name, create_component_by_master_page_name
from .strategies.boundary.impl import boundary_identifier_by_curved_panel
