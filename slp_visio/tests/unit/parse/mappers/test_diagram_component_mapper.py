from unittest.mock import MagicMock

import pytest

from slp_visio.slp_visio.load.objects.diagram_objects import DiagramComponent

from slp_base import MappingFileNotValidError
from slp_visio.slp_visio.parse.mappers.diagram_component_mapper import DiagramComponentMapper

tz1 = DiagramComponent(id='tz1')
c1 = DiagramComponent(id='c1', name='Component 1')
c1.parent = tz1
c2 = DiagramComponent(id='c2', name='Component 2')
c2.parent = c1
c3 = DiagramComponent(id='c3', name='3')
c3.parent = None
c4 = DiagramComponent(id='c4', name='Component 4')


diagram_components = [tz1, c1, c2, c3, c4]


component_mappings = {
    c1.id: {'type': 'type-1'},
    c2.id: {'type': 'type-2'},
    c3.id: {'type': 'type-3'},
}

trustzone_mappings = {
    tz1.id: {'type': 'type-1'}
}

default_trustzone = MagicMock(id='1', type='default-trustzone')

representation_calculator = MagicMock(calculate_representation=MagicMock())


class TestDiagramComponentMapper:

    def test_to_otm(self):
        # GIVEN the diagram component mapper
        diagram_component_mapper = DiagramComponentMapper(
            diagram_components,
            component_mappings,
            trustzone_mappings,
            default_trustzone,
            representation_calculator
        )

        # WHEN to_otm is called
        components = diagram_component_mapper.to_otm()

        # THEN the components are mapped correctly
        assert len(components) == 3
        assert components[0].id == 'c1'
        assert components[0].type == 'type-1'
        assert components[0].parent == 'tz1'
        assert components[0].name == c1.name

        assert components[1].id == 'c2'
        assert components[1].type == 'type-2'
        assert components[1].parent == 'c1'
        assert components[1].name == c2.name

        assert components[2].id == 'c3'
        assert components[2].type == 'type-3'
        assert components[2].parent == default_trustzone.id
        assert components[2].name == f"_{c3.name}"

    def test_not_default_trustzone(self):
        # GIVEN the diagram component mapper without a default trustzone
        diagram_component_mapper = DiagramComponentMapper(
            diagram_components,
            component_mappings,
            trustzone_mappings,
            None,
            representation_calculator
        )

        # WHEN to_otm is called, expect an exception
        with pytest.raises(MappingFileNotValidError) as error:
            diagram_component_mapper.to_otm()

        # THEN an exception is raised
        assert error.value.title == 'Mapping files are not valid'
        assert error.value.detail == 'No default trust zone has been defined in the mapping file'
        assert error.value.message == 'Please, add a default trust zone'