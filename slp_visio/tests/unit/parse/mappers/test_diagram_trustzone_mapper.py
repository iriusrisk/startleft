from unittest.mock import MagicMock

from otm.otm.entity.parent_type import ParentType
from slp_visio.slp_visio.parse.mappers.diagram_trustzone_mapper import DiagramTrustzoneMapper

tz1 = MagicMock(id='tz1')
tz1.parent = None
tz2 = MagicMock(id='tz2')
tz2.parent = tz1
tz3 = MagicMock(id='tz3')

diagram_components = [tz1, tz2, tz3]

trustzone_mappings = {
    tz1.id: {'id': 'type-1'},
    tz2.id: {'type': 'type-2'},
}

representation_calculator = MagicMock(calculate_representation=MagicMock())


class TestDiagramTrustzoneMapper:

    def test_otm_type(self):
        # GIVEN the diagram trustzone mapper
        diagram_trustzone_mapper = DiagramTrustzoneMapper(
            diagram_components,
            trustzone_mappings,
            representation_calculator
        )

        # WHEN to_otm is called
        trustzones = diagram_trustzone_mapper.to_otm()

        # THEN the trustzones are mapped correctly
        assert len(trustzones) == 2
        assert trustzones[0].id == 'tz1'
        assert trustzones[0].type == 'type-1'
        assert trustzones[0].parent is None
        assert trustzones[0].parent_type == ParentType.TRUST_ZONE

        assert trustzones[1].id == 'tz2'
        assert trustzones[1].type == 'type-2'
        assert trustzones[1].parent == tz1.id
        assert trustzones[1].parent_type == ParentType.TRUST_ZONE
