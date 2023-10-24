from typing import List

from pytest import mark, param

from slp_drawio.slp_drawio.load.drawio_mapping_file_loader import DrawioMapping
from slp_drawio.slp_drawio.objects.diagram_objects import DiagramComponent, DiagramTrustZone
from slp_drawio.slp_drawio.parse.diagram_mapper import DiagramMapper
from slp_drawio.tests.util.builders import build_diagram, build_component, build_components

DEFAULT_COMPONENT_TYPE = 'empty-component'


def _tz_mapping(label: str = 'label', _type: str = 'type', default: bool = False):
    return {
        'label': label,
        'type': _type,
        'default': default
    }


class TestDiagramMapper:

    @mark.parametrize('trustzone_mappings,expected_tz_index', [
        param([_tz_mapping(), _tz_mapping(_type='tz-type', default=True)], 1, id='default trustzone'),
        param([_tz_mapping(_type='type-1'), _tz_mapping(_type='type-2')], 0, id='no default trustzones'),
        param([], None, id='no trustzones'),
    ])
    def test_default_trustzone_creation(self, trustzone_mappings: List[dict], expected_tz_index: int):
        # GIVEN a Drawio mapping with or without some trustzones
        mapping = DrawioMapping(trustzones=trustzone_mappings, components=[])

        # AND a diagram
        diagram = build_diagram()

        # WHEN DiagramMapper::map is invoked
        DiagramMapper(project_id='id', diagram=diagram, mapping=mapping).map()

        # THEN the default trustzone is created by the flag or the first one otherwise
        assert bool(diagram.default_trustzone) == bool(expected_tz_index)
        if diagram.default_trustzone:
            expected_tz_mapping = trustzone_mappings[expected_tz_index]
            assert diagram.default_trustzone.otm.type == expected_tz_mapping['type']
            assert diagram.default_trustzone.otm.id == f'default-{diagram.default_trustzone.otm.type}'
            assert diagram.default_trustzone.otm.name == expected_tz_mapping['label']

    @mark.parametrize('component,component_mapping', [
        param(build_component(name='simple-name'), {'label': 'simple-name', type: 'otm-type'}, id='by exact name'),
        param(build_component(name='simple-name-1'), {'label': r'simple-name(-1)?', type: 'otm-type'},
              id='by regex name'),
        param(build_component(shape_type='shape_type'), {'label': 'shape_type', type: 'otm-type'}, id='by exact type'),
        param(build_component(shape_type='simple-name-1'), {'label': r'shape_type(-1)?', type: 'otm-type'},
              id='by regex type')
    ])
    def test_mapping_components(self, component: DiagramComponent, component_mapping: dict):
        # GIVEN a Diagram with some components with different names and types
        diagram = build_diagram(components=[component])

        # AND a DrawioMapping with some component mappings matching by exact name/type or regex
        mapping = DrawioMapping(trustzones=[], components=[component_mapping])

        # WHEN DiagramMapper::map is invoked
        DiagramMapper(project_id='id', diagram=diagram, mapping=mapping).map()

        # THEN the type of the components are changed giving priority to mappings by name
        assert component.otm.type == component_mapping['type']

    @mark.parametrize('component,trustzone_mapping', [
        param(build_component(name='simple-name'), {'label': 'simple-name', type: 'otm-type'}, id='by exact name'),
        param(build_component(name='simple-name-1'), {'label': r'simple-name(-1)?', type: 'otm-type'},
              id='by regex name'),
        param(build_component(shape_type='shape_type'), {'label': 'shape_type', type: 'otm-type'}, id='by exact type'),
        param(build_component(shape_type='simple-name-1'), {'label': r'shape_type(-1)?', type: 'otm-type'},
              id='by regex type')
    ])
    def test_mapping_trustzones(self, component: DiagramComponent, trustzone_mapping: dict):
        # GIVEN a Diagram with some components with different names and types
        diagram = build_diagram(components=[component])

        # AND a DrawioMapping with some trustzone mappings matching by exact name/type or regex
        mapping = DrawioMapping(trustzones=[trustzone_mapping], components=[])

        # WHEN DiagramMapper::map is invoked
        DiagramMapper(project_id='id', diagram=diagram, mapping=mapping).map()

        # THEN the component is converted into a trustzone
        assert component not in diagram.components
        assert len(diagram.trustzones) == 1

        # AND the trustzone is well configured
        trustzone = diagram.trustzones[0]
        assert isinstance(trustzone, DiagramTrustZone)
        assert trustzone.otm.id == component.otm.id
        assert trustzone.otm.name == component.otm.name
        assert trustzone.otm.type == trustzone_mapping['type']

    def test_name_over_type_mapping(self):
        # GIVEN two different mappings
        mapping_by_name = {'label': 'name', 'type': 'type-1'}
        mapping_by_type = {'label': 'type', 'type': 'type-2'}
        mapping = DrawioMapping(components=[mapping_by_name, mapping_by_type], trustzones=[])

        # AND a component whose type match one mapping and its name another
        component = build_component(name='name', shape_type='type')

        # WHEN DiagramMapper::map is invoked
        DiagramMapper(project_id='id', diagram=build_diagram(components=[component]), mapping=mapping).map()

        # THEN the mapping by name prevails
        assert component.otm.type == mapping_by_name['type']

    def test_trustzone_over_component(self):
        # GIVEN the same mapping in for trustzones and components
        mapping_by_name = {'label': 'name', 'type': 'otm-type'}
        mapping = DrawioMapping(components=[mapping_by_name], trustzones=[mapping_by_name])

        # AND a Diagram with a component matching that map
        component = build_component(component_id='id', name='name')
        diagram = build_diagram(components=[component])

        # WHEN DiagramMapper::map is invoked
        DiagramMapper(project_id='id', diagram=diagram, mapping=mapping).map()

        # THEN the trustzone mapping prevails
        assert component not in diagram.components
        assert len(diagram.trustzones) == 1
        assert isinstance(diagram.trustzones[0], DiagramTrustZone)
        assert diagram.trustzones[0].otm.type == mapping_by_name['type']

    def test_non_mapped_components(self):
        # GIVEN some components that cannot be mapped
        no_shape_type_component = build_component(component_id='nst')
        unmapped_type_component = build_component(component_id='nmt', shape_type='no-mapped')
        components = [no_shape_type_component, unmapped_type_component]

        # AND no matching mappings
        non_matching_mapping = {'label': 'label', 'type': 'type'}
        mapping = DrawioMapping(components=[non_matching_mapping], trustzones=[non_matching_mapping])

        # WHEN DiagramMapper::map is invoked
        DiagramMapper(project_id='id', diagram=build_diagram(components=components), mapping=mapping).map()

        # THEN their type is set to the default one
        for component in components:
            assert component.otm.type == DEFAULT_COMPONENT_TYPE

    def test_no_mappings(self):
        # GIVEN a diagram with some components
        components = build_components(3)
        diagram = build_diagram(components=components)

        # AND a Drawio mapping with no mappings
        mapping = DrawioMapping(components=[], trustzones=[])

        # WHEN DiagramMapper::map is invoked
        DiagramMapper(project_id='id', diagram=diagram, mapping=mapping).map()

        # THEN all the components are mapped to the default component type
        for component in components:
            assert component.otm.type == DEFAULT_COMPONENT_TYPE

        # AND no default trustzone is added
        assert not diagram.default_trustzone

    def test_no_components(self):
        # GIVEN a diagram with no components
        diagram = build_diagram(components=[])

        # AND a DrawioMapping with mappings
        # AND a default trustzone
        default_trustzone_mapping = _tz_mapping(default=True)
        mapping = DrawioMapping(components=[{'label': 'label', 'type': 'type'}], trustzones=[default_trustzone_mapping])

        # WHEN DiagramMapper::map is invoked
        DiagramMapper(project_id='id', diagram=diagram, mapping=mapping).map()

        # THEN no components are added
        assert not diagram.components

        # AND the default trustzone is added
        assert diagram.default_trustzone.type == default_trustzone_mapping['type']
