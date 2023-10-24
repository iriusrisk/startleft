from typing import List, Dict
from unittest.mock import patch

from pytest import mark, param

from slp_drawio.slp_drawio.load.drawio_mapping_file_loader import DrawioMapping
from slp_drawio.slp_drawio.objects.diagram_objects import DiagramComponent, DiagramTrustZone
from slp_drawio.slp_drawio.parse import diagram_mapper
from slp_drawio.slp_drawio.parse.diagram_mapper import DiagramMapper, _find_mapping
from slp_drawio.tests.util.builders import build_diagram, build_component, build_components

DEFAULT_COMPONENT_TYPE = 'empty-component'


def _tz_mapping(label: str = 'label', _type: str = 'type', default: bool = False):
    return {
        'label': label,
        'type': _type,
        'default': default
    }


@mark.parametrize('component_label,mapping,expected_match', [
    param('simple-label', {'label': 'simple-label'}, True, id='by exact match'),
    param('no-match', {'label': 'simple-label'}, False, id='no exact match'),
    param('regex-label-1', {'label': {'$regex': r'regex-label(-1)?'}}, True, id='by regex'),
    param('no-match', {'label': {'$regex': r'regex-label(-1)?'}}, False, id='no match regex'),
    param('label-1', {'label': ['label-1', 'label-2']}, True, id='by list'),
    param('no-match', {'label': ['label-1', 'label-2']}, False, id='no match list')
])
def test_find_mapping(component_label: str, mapping: Dict, expected_match: bool):
    # GIVEN a component label
    # AND a mapping

    # WHEN diagram_mapper:: _find_mapping
    mapping_match = diagram_mapper._find_mapping(component_label, [mapping])

    # THEN a mapping is returned if it matches the component label
    if expected_match:
        assert mapping_match == mapping
    else:
        assert not mapping_match


class TestDiagramMapper:

    @mark.parametrize('trustzone_mappings,expected_tz_index', [
        param([_tz_mapping(), _tz_mapping(_type='tz-type', default=True)], 1, id='default trustzone'),
        param([_tz_mapping(_type='tz-type'), _tz_mapping(_type='type-2')], 0, id='no default trustzone'),
        param([], None, id='no trustzones'),
    ])
    def test_default_trustzone_creation(self, trustzone_mappings: List[dict], expected_tz_index: int):
        # GIVEN a Drawio mapping with or without some trustzones
        mapping = DrawioMapping(trustzones=trustzone_mappings, components=[])

        # AND a diagram
        diagram = build_diagram()

        # WHEN DiagramMapper::map is invoked
        DiagramMapper(diagram=diagram, mapping=mapping).map()

        # THEN the default trustzone is created by the flag or the first one otherwise
        assert bool(diagram.default_trustzone) == bool(expected_tz_index is not None)
        if diagram.default_trustzone:
            expected_tz_mapping = trustzone_mappings[expected_tz_index]
            assert diagram.default_trustzone.otm.type == expected_tz_mapping['type']
            # deterministic_uuid(f'default-{trustzone_mapping["type"]}')
            assert diagram.default_trustzone.otm.id == 'b8cc60fb-ab2c-4910-baa9-17b2f141eab1'
            assert diagram.default_trustzone.otm.name == expected_tz_mapping['label']

    @patch('slp_drawio.slp_drawio.parse.diagram_mapper._find_mapping', wraps=_find_mapping)
    @mark.parametrize('component,mappings,find_call_count,expected_type', [
        param(build_component(name='simple-name'), [{'label': 'simple-name', 'type': 'otm-type'}], 1, 'otm-type',
              id='by name'),
        param(build_component(shape_type='type'), [{'label': 'type', 'type': 'otm-type'}], 2, 'otm-type',
              id='by type'),
        param(build_component(name='name', shape_type='type'),
              [{'label': 'type', 'type': 'otm-type-1'}, {'label': 'name', 'type': 'otm-type-2'}], 1, 'otm-type-2',
              id='by name and type'),
        param(build_component(name='no-match'), [{'label': 'simple-name', 'type': 'otm-type'}], 2,
              DEFAULT_COMPONENT_TYPE, id='not match')
    ])
    def test_mapping_components(self, find_mapping_wrapper, component: DiagramComponent, mappings: List,
                                find_call_count, expected_type):
        # GIVEN a Diagram with some components with different names and types
        diagram = build_diagram(components=[component])

        # AND a DrawioMapping with some component mappings matching by exact name/type or regex
        drawio_mapping = DrawioMapping(trustzones=[], components=mappings)

        # WHEN DiagramMapper::map is invoked
        DiagramMapper(diagram=diagram, mapping=drawio_mapping).map()

        # THEN the type of the components are changed giving priority to mappings by name
        assert find_mapping_wrapper.call_count == find_call_count
        assert component.otm.type == expected_type

    @patch('slp_drawio.slp_drawio.parse.diagram_mapper._find_mapping', wraps=_find_mapping)
    @mark.parametrize('component,mappings,find_call_count,expected_type', [
        param(build_component(name='simple-name'), [{'label': 'simple-name', 'type': 'otm-type'}], 1, 'otm-type',
              id='by name'),
        param(build_component(shape_type='type'), [{'label': 'type', 'type': 'otm-type'}], 2, 'otm-type',
              id='by type'),
        param(build_component(name='name', shape_type='type'),
              [{'label': 'type', 'type': 'otm-type-1'}, {'label': 'name', 'type': 'otm-type-2'}], 1, 'otm-type-2',
              id='by name and type')
    ])
    def test_mapping_trustzones(self, find_mapping_wrapper, component: DiagramComponent, mappings: List,
                                find_call_count, expected_type):
        # GIVEN a Diagram with some components with different names and types
        diagram = build_diagram(components=[component])

        # AND a DrawioMapping with some trustzone mappings matching by exact name/type or regex
        mapping = DrawioMapping(trustzones=mappings, components=[])

        # WHEN DiagramMapper::map is invoked
        DiagramMapper(diagram=diagram, mapping=mapping).map()

        # THEN the component is converted into a trustzone
        assert find_mapping_wrapper.call_count == find_call_count

        assert component not in diagram.components
        assert len(diagram.trustzones) == 1

        # AND the trustzone is well configured
        trustzone = diagram.trustzones[0]
        assert isinstance(trustzone, DiagramTrustZone)
        assert trustzone.otm.id == component.otm.id
        assert trustzone.otm.name == component.otm.name
        assert trustzone.otm.type == expected_type
        assert component.shape_parent_id == trustzone.shape_parent_id
        assert component.shape_type == trustzone.shape_type

    def test_trustzone_over_component(self):
        # GIVEN the same mapping in for trustzones and components
        mapping_by_name = {'label': 'name', 'type': 'otm-type'}
        mapping = DrawioMapping(components=[mapping_by_name], trustzones=[mapping_by_name])

        # AND a Diagram with a component matching that map
        component = build_component(component_id='id', name='name')
        diagram = build_diagram(components=[component])

        # WHEN DiagramMapper::map is invoked
        DiagramMapper(diagram=diagram, mapping=mapping).map()

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
        DiagramMapper(diagram=build_diagram(components=components), mapping=mapping).map()

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
        DiagramMapper(diagram=diagram, mapping=mapping).map()

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
        DiagramMapper(diagram=diagram, mapping=mapping).map()

        # THEN no components are added
        assert not diagram.components

        # AND the default trustzone is added
        assert diagram.default_trustzone.otm.type == default_trustzone_mapping['type']
