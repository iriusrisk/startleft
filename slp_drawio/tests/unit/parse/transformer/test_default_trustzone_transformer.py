from typing import List
from unittest.mock import patch

from pytest import mark, param, raises

from otm.otm.entity.parent_type import ParentType
from slp_base import OTMBuildingError
from slp_drawio.slp_drawio.objects.diagram_objects import DiagramTrustZone
from slp_drawio.slp_drawio.parse.transformer.default_trustzone_transformer import DefaultTrustZoneTransformer
from slp_drawio.tests.util.builders import build_component, build_diagram, build_components

DEFAULT_TRUSTZONE: DiagramTrustZone = DiagramTrustZone(type_='dtz', id_='dtz', name='Default TrustZone', default=True)


class TestDefaultTrustZoneTransformer:
    @patch('slp_drawio.slp_drawio.parse.transformer.default_trustzone_transformer.TrustZoneRepresentationCalculator')
    def test_some_orphan_components(self, repr_calc_mock):
        # GIVEN a Diagram with default trustzone
        default_trustzone = DEFAULT_TRUSTZONE

        # AND a trustzone with a nested trustzone
        trustzone = DiagramTrustZone('tz', 'tz')

        nested_trustzone = DiagramTrustZone('ntz', 'ntz')
        nested_trustzone.otm.parent = trustzone.otm.id
        nested_trustzone.otm.parent_type = ParentType.TRUST_ZONE

        trustzones = [trustzone, nested_trustzone]

        # AND some DiagramComponents with parents and others without
        components_with_parent = build_components(count=5, orphan=False)
        orphan_components = build_components(count=5, orphan=True)

        diagram = build_diagram(
            default_trustzone=default_trustzone,
            trustzones=trustzones,
            components=components_with_parent + orphan_components)

        # WHEN DefaultTrustZoneTransformer::transform is invoked
        DefaultTrustZoneTransformer(diagram).transform()

        # THEN the default trustzone is added to the diagram
        assert DEFAULT_TRUSTZONE in diagram.trustzones

        # AND the nested trustzone remains without changes
        assert nested_trustzone.otm.parent == trustzone.otm.id
        assert nested_trustzone.otm.parent_type == ParentType.TRUST_ZONE

        # AND the components with parents remain without changes
        assert len(diagram.components) == 10
        assert diagram.components[:5] == components_with_parent

        # AND the orphan trustzone is now child of the default one
        assert trustzone.otm.parent == default_trustzone.otm.id
        assert trustzone.otm.parent_type == ParentType.TRUST_ZONE

        # AND all the orphan DiagramComponents in the Diagram have now the default DiagramTrustZone as the parent
        for orphan_component in orphan_components:
            assert orphan_component.otm.parent_type == ParentType.TRUST_ZONE
            assert orphan_component.otm.parent == DEFAULT_TRUSTZONE.otm.id

        # AND a representation is calculated for the DiagramTrustZone matching the limits of its children
        expected_representation_id = diagram.representation.otm.id
        orphan_components_otms = [c.otm for c in orphan_components]
        orphan_trustzones_otms = [trustzone.otm]

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
        trustzone = DiagramTrustZone(id_='tz', name='tz', type_='tzt')
        components = [build_component(component_id='c', parent_id=trustzone.otm.id)]
        diagram = build_diagram(
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
        param([DiagramTrustZone('tz')], id='with trustzones'),
        param(None, id='without trustzones')
    ])
    def test_orphan_components_and_no_default_trustzone(self, trustzones: List[DiagramTrustZone]):
        # GIVEN a Diagram with no TrustZones
        # AND some orphan components
        diagram = build_diagram(trustzones=trustzones, components=build_components(count=5, orphan=True))

        # WHEN DefaultTrustZoneTransformer::transform is invoked
        # THEN an error is raised
        with raises(OTMBuildingError) as error:
            DefaultTrustZoneTransformer(diagram).transform()

        # AND an empty IaC file message is on the exception
        assert error.value.title == 'Invalid configuration'
        assert error.value.message == 'A default trust zone is required with orphan components'
