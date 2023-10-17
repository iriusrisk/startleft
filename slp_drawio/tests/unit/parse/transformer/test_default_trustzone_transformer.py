from typing import List
from unittest.mock import patch

from pytest import mark, param, raises

from otm.otm.entity.parent_type import ParentType
from otm.otm.entity.representation import RepresentationElement
from slp_base import OTMBuildingError
from slp_drawio.slp_drawio.objects.diagram_objects import Diagram, DiagramTrustZone, DiagramComponent
from slp_drawio.slp_drawio.parse.transformer.default_trustzone_transformer import DefaultTrustZoneTransformer

DEFAULT_TRUSTZONE: DiagramTrustZone = DiagramTrustZone('dtz', 'Default TrustZone', True)


def _create_diagram(default_trustzone: DiagramTrustZone = None, trustzones: List[DiagramTrustZone] = None,
                    components: List[DiagramComponent] = None):
    return Diagram(
        default_trustzone=default_trustzone,
        trustzones=trustzones,
        components=components,
        representation=RepresentationElement('repr-id', 'repr-name', 'repr-id'))


def _create_components(count: int, orphan: bool = False) -> List[DiagramComponent]:
    return list(map(
        lambda c_id: _create_component(f'{c_id}', None if orphan else f'p-{c_id}'),
        range(1, count + 1)))


def _create_component(component_id: str, parent_id: str = None) -> DiagramComponent:
    component = DiagramComponent(id=component_id, name=component_id)
    component.otm.parent = parent_id
    return component


class TestDefaultTrustZoneTransformer:
    @patch('slp_drawio.slp_drawio.parse.transformer.default_trustzone_transformer.TrustZoneRepresentationCalculator')
    def test_some_orphan_components(self, repr_calc_mock):
        # GIVEN a Diagram with default trustzone
        default_trustzone = DEFAULT_TRUSTZONE

        # AND other trustzones
        trustzones = [DiagramTrustZone('tz1', 'tz1'), DiagramTrustZone('tz2', 'tz2')]

        # AND some DiagramComponents with parents and others without
        components_with_parent = _create_components(count=5, orphan=False)
        orphan_components = _create_components(count=5, orphan=True)

        diagram = _create_diagram(
            default_trustzone=default_trustzone,
            trustzones=trustzones,
            components=components_with_parent + orphan_components)

        # WHEN DefaultTrustZoneTransformer::transform is invoked
        DefaultTrustZoneTransformer(diagram).transform()

        # THEN the default trustzone is added to the diagram
        assert DEFAULT_TRUSTZONE in diagram.trustzones

        # AND the components with parents remain without changes
        assert len(diagram.components) == 10
        assert diagram.components[:5] == components_with_parent

        # AND all the orphan DiagramComponents in the Diagram have now the default DiagramTrustZone as the parent
        for orphan_component in orphan_components:
            assert orphan_component.otm.parent_type == ParentType.TRUST_ZONE
            assert orphan_component.otm.parent == DEFAULT_TRUSTZONE.otm.id

        # AND a representation is calculated for the DiagramTrustZone matching the limits of its children
        expected_representation_id = diagram.representation.id
        orphan_components_otms = [c.otm for c in orphan_components]
        orphan_trustzones_otms = [tz.otm for tz in trustzones if tz.otm.id != default_trustzone.otm.id]

        repr_calc_mock.assert_called_once_with(
            representation_id=expected_representation_id,
            trustzone=DEFAULT_TRUSTZONE.otm,
            children=orphan_components_otms + orphan_trustzones_otms)

        repr_calc_mock.return_value.calculate.assert_called_once()

    @mark.parametrize('default_trustzone', [
                      param(DEFAULT_TRUSTZONE, id='with default trustzone'),
                      param(None, id='without default trustzone')])
    def test_no_orphan_components(self, default_trustzone: DiagramTrustZone):
        # GIVEN a Diagram with a DiagramTrustZone set as default
        # AND some DiagramComponents all of them with the parent set
        trustzone = DiagramTrustZone(id='tz', name='tz', type='tzt')
        components = [_create_component(component_id='c', parent_id=trustzone.otm.id)]
        diagram = _create_diagram(
            components=components,
            default_trustzone=default_trustzone,
            trustzones=[trustzone]
        )

        # WHEN DefaultTrustZoneTransformer::transform is invoked
        DefaultTrustZoneTransformer(diagram).transform()

        # THEN no DiagramComponent is modified
        assert diagram.components == components

        # AND the default trustzone is not added to the diagram
        assert DEFAULT_TRUSTZONE not in diagram.trustzones

    @mark.parametrize('trustzones', [
        param([DiagramTrustZone('tz')] , id='with trustzones'),
        param(None, id='without trustzones')
    ])
    def test_orphan_components_and_no_default_trustzone(self, trustzones: List[DiagramTrustZone]):
        # GIVEN a Diagram with no TrustZones
        # AND some orphan components
        diagram = _create_diagram(trustzones=trustzones, components=_create_components(count=5, orphan=True))

        # WHEN DefaultTrustZoneTransformer::transform is invoked
        # THEN an error is raised
        with raises(OTMBuildingError) as error:
            DefaultTrustZoneTransformer(diagram).transform()

        # AND an empty IaC file message is on the exception
        assert error.value.title == 'Invalid configuration'
        assert error.value.message == 'A default trust zone is required with orphan components'
