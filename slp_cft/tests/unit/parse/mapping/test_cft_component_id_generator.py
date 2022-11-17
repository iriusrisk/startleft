from pytest import mark

from slp_cft.slp_cft.parse.mapping.cft_component_id_generator import CloudformationComponentIdGenerator

SAMPLE_NAME = 'sample_name'
SAMPLE_TYPE = 'sample_type'
SAMPLE_PARENT_ID = 'b61d6911-338d-46a8-9f39-8dcd24abfe91'

NAMES_PARENT_USE_CASES = [
    (SAMPLE_NAME, SAMPLE_PARENT_ID, SAMPLE_NAME),
    ('0.0.0.0', 'parent_name', '0_0_0_0'),
    ('Sample_Name', 'parent_name-altsource', 'sample_name'),
    ('hyphens-name', f'{SAMPLE_PARENT_ID}.parent_name1.parent_name2', 'hyphens_name')
]


def build_source_sample(component_name: str, component_type: str, is_altsource: bool = False):
    return {
        component_name: {},
        'Type': component_type,
        '_key': component_name,
        'altsource': is_altsource
    }


class TestCloudformationComponentIdGenerator:

    @mark.parametrize('name, parent_id, expected_name', NAMES_PARENT_USE_CASES)
    def test_build_generator_from_regular_component_names(self, name, parent_id, expected_name):
        # GIVEN a component source dictionary
        component_source = build_source_sample(name, SAMPLE_TYPE)

        # WHEN from_regular_component is called
        id_generator = CloudformationComponentIdGenerator.from_component(component_source, parent_id)

        # THEN a CloudformationComponentIdGenerator is created
        # AND the altsource flag is False
        assert not id_generator.is_altsource

        # AND the component information is present
        assert id_generator.name == expected_name
        assert id_generator.type == component_source['Type']
        assert id_generator.parent_id == parent_id

    @mark.parametrize('name, parent_id, expected_name', NAMES_PARENT_USE_CASES)
    def test_build_generator_from_alsource_names(self, name, parent_id, expected_name):
        # GIVEN a altsource object dictionary
        component_source = build_source_sample(name, SAMPLE_TYPE, is_altsource=True)

        # WHEN from_altsource_component is called
        id_generator = CloudformationComponentIdGenerator.from_component(component_source, parent_id)

        # THEN a TerraformComponentIdGenerator is created
        # AND the altsource flag is True
        assert id_generator.is_altsource

        # AND the component information is present
        assert id_generator.name == expected_name
        assert id_generator.type == component_source['Type']
        assert id_generator.parent_id == parent_id

    def test_generate_id_generic_component(self):
        # GIVEN a component name
        name = SAMPLE_NAME

        # AND some type
        component_type = SAMPLE_TYPE

        # AND a parent_id
        parent_id = SAMPLE_PARENT_ID

        # WHEN generate_id is called
        component_id = CloudformationComponentIdGenerator(name=name, parent_id=parent_id, type=component_type).generate_id()

        # THEN the ID is generated with the right format
        assert component_id == f'{parent_id}.{name}'

    def test_generate_id_altsource(self):
        # GIVEN an altsource component name
        name = SAMPLE_NAME

        # AND some type
        component_type = SAMPLE_TYPE

        # AND a parent_id
        parent_id = SAMPLE_PARENT_ID

        # WHEN generate_id is called
        component_id = CloudformationComponentIdGenerator(name=name, parent_id=parent_id, type=component_type, is_altsource=True).generate_id()

        # THEN the ID is generated with the right format
        assert component_id == f'{parent_id}.{name}-altsource'

    @mark.parametrize('name, parent_id, expected_name', [
        ('0.0.0.0/0', 'tz1', '0_0_0_0_0'),
        ('52.30.97.44/32', 'tz1', '52_30_97_44_32')])
    def test_generate_id_components_from_same_resource(self, name, parent_id, expected_name):
        # GIVEN a component source dictionary of type AWS::EC2::SecurityGroup
        component_source = build_source_sample(name, 'AWS::EC2::SecurityGroup')

        # WHEN from_component is called
        id_generator = CloudformationComponentIdGenerator.from_component(component_source, parent_id, name)

        # AND an id is generated
        generated_id = id_generator.generate_id()

        # THEN the ID is generated with the right format
        assert generated_id == f'{parent_id}.{expected_name}.{expected_name}'

        # AND the component information is present
        assert id_generator.name == expected_name
        assert id_generator.type == component_source['Type']
        assert id_generator.parent_id == parent_id
