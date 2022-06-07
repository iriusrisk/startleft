import os

path = os.path.dirname(__file__)

default_cf_mapping_file = os.path.join(path, 'resources/defaultmappings/default-cloudformation-mapping.yaml')
default_tf_mapping_file = os.path.join(path, 'resources/defaultmappings/default-terraform-mapping.yaml')
default_visio_mapping_file = os.path.join(path, 'resources/defaultmappings/default-visio-mapping.yaml')

otm_schema = os.path.join(path, 'resources/schemas/otm_schema.json')
iac_schema = os.path.join(path, 'resources/schemas/iac_mapping_schema.json')
diagram_schema = os.path.join(path, 'resources/schemas/diagram_mapping_schema.json')
