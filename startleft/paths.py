import os

path = os.path.dirname(__file__)

default_cf_mapping_file = os.path.join(path, 'config/default-cloudformation-mapping.yaml')
default_tf_mapping_file = os.path.join(path, 'config/default-terraform-mapping.yaml')
default_visio_mapping_file = os.path.join(path, 'config/default-visio-mapping.yaml')

otm_schema = os.path.join(path, 'data/otm_schema.json')
iac_schema = os.path.join(path, 'data/iac_mapping_schema.json')
diagram_schema = os.path.join(path, 'data/diagram_mapping_schema.json')
