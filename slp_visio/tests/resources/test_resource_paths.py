import os

path = os.path.dirname(__file__)

# generic
invalid_yaml = f'{path}/generic/invalid-yaml.yaml'

# mapping
default_visio_mapping = f'/{path}/mapping/aws-visio-mapping.yaml'
custom_vpc_mapping = f'/{path}/mapping/custom-vpc-mapping.yaml'
empty_mapping = f'/{path}/mapping/empty-mapping.yaml'

# legacy mapping
default_visio_mapping_legacy = path + '/mapping/legacy/aws-visio-mapping.yaml'
custom_vpc_mapping_legacy = path + '/mapping/legacy/custom-vpc-mapping.yaml'

# visio
visio_aws_with_tz_and_vpc = f'{path}/visio/aws-with-tz-and-vpc.vsdx'
visio_aws_shapes = f'{path}/visio/aws-shapes.vsdx'
visio_aws_stencils = f'{path}/visio/aws-stencils.vsdx'
visio_generic_shapes = f'{path}/visio/generic-shapes.vsdx'
visio_self_pointing_connectors = f'{path}/visio/self-pointing-connectors.vsdx'
visio_extraneous_elements = f'{path}/visio/extraneous-elements.vsdx'
visio_boundaries = f'{path}/visio/boundaries.vsdx'
visio_simple_boundary_tzs = f'{path}/visio/simple-boundary-tzs.vsdx'
visio_boundary_tz_and_default_tz = f'{path}/visio/boundary-tz-and-default-tz.vsdx'
visio_overlapped_boundary_tzs = f'{path}/visio/overlapped-boundary-tzs.vsdx'
visio_multiple_pages_diagram = f'{path}/visio/multiple-pages-diagram.vsdx'
visio_boundary_and_component_tzs = f'{path}/visio/boundary-and-component-tzs.vsdx'
visio_nested_tzs = f'{path}/visio/nested-tzs.vsdx'
visio_simple_components = f'{path}/visio/simple-components.vsdx'
visio_orphan_dataflows = f'{path}/visio/visio-orphan-dataflows.vsdx'
visio_invalid_file_size = f'{path}/visio/invalid-file-size.vsdx'
visio_invalid_file_type = f'{path}/visio/invalid-file-type.pdf'
visio_modified_single_connectors = f'{path}/visio/modified-single-connectors.vsdx'
visio_bidirectional_connectors = f'{path}/visio/bidirectional-connectors.vsdx'
visio_complex_stencil_text = f'{path}/visio/standalone-with-custom-name-AWS-complex-stencils-shapes.vsdx'
visio_empty = f'{path}/visio/empty-diagram.vsdx'

# otm
expected_aws_shapes = f'{path}/otm/expected_aws_shapes.otm'
expected_bidirectional_connectors = f'{path}/otm/expected_bidirectional_connectors.otm'
expected_boundary_tz_and_default_tz = f'{path}/otm/expected_boundary_tz_and_default_tz.otm'
expected_complex_diagram = f'{path}/otm/expected_complex_diagram.otm'
expected_empty_mapping_and_visio_files = f'{path}/otm/expected_empty_mapping_and_visio_files.otm'
expected_empty_mapping_file = f'{path}/otm/expected_empty_mapping_file.otm'
expected_empty_visio_file = f'{path}/otm/expected_empty_visio_file.otm'
expected_extraneous_elements = f'{path}/otm/expected_extraneous_elements.otm'
expected_generic_elements = f'{path}/otm/expected_generic_elements.otm'
expected_manually_modified_connectors = f'{path}/otm/expected_manually_modified_connectors.otm'
expected_multiple_pages_diagram = f'{path}/otm/expected_multiple_pages_diagram.otm'
expected_overlapped_boundary_tzs = f'{path}/otm/expected_overlapped_boundary_tzs.otm'
expected_prune_orphan_connectors = f'{path}/otm/expected_prune_orphan_connectors.otm'
expected_self_pointing_connectors = f'{path}/otm/expected_self_pointing_connectors.otm'
expected_simple_boundary_tzs = f'{path}/otm/expected_simple_boundary_tzs.otm'
expected_visio_boundary_and_component_tzs = f'{path}/otm/expected_visio_boundary_and_component_tzs.otm'