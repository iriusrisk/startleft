from pytest import mark

from otm.otm.entity.representation import DiagramRepresentation, RepresentationType, RepresentationElement
from slp_mtmt.slp_mtmt.parse.mtmt_trustzone_parser import MTMTTrustzoneParser
from slp_mtmt.tests.mtmt_test_utils import get_mtmt_from_file, get_mapping_from_file
from slp_mtmt.tests.resources import test_resource_paths
from slp_mtmt.tests.resources.test_resource_paths import mapping_mtmt_mvp, model_mtmt_mvp, mapping_mtmt_mvp_legacy, \
    mtmt_default_mapping, mtmt_default_mapping_legacy, mapping_mtmt_mvp_no_type, mtmt_default_mapping_no_type, \
    nested_trustzones_tm7

diagram_representation = DiagramRepresentation(id_='project-test-diagram',
                                               name='Project Test Diagram Representation',
                                               type_=RepresentationType.DIAGRAM,
                                               size={'width': 2000, 'height': 2000}
                                               )


class TestMTMTTrustzoneParser:

    def test_parse_with_empty_mapping_file(self):
        # GIVEN the Mtmt data
        mtmt = get_mtmt_from_file(test_resource_paths.model_mtmt_mvp)

        # AND the mapping data
        mtmt_mapping = get_mapping_from_file(test_resource_paths.mtmt_empty_mapping_file)

        # THEN a MtmtMapping is returned with no trustzones
        mtmt_trustzone_parser = MTMTTrustzoneParser(mtmt, mtmt_mapping, diagram_representation.id)
        trustzones = mtmt_trustzone_parser.parse()

        assert len(trustzones) == 0

    @mark.parametrize('mapping_file', [mapping_mtmt_mvp, mapping_mtmt_mvp_legacy, mapping_mtmt_mvp_no_type])
    def test_parse_with_filled_mapping_file(self, mapping_file):
        # GIVEN the Mtmt data
        mtmt = get_mtmt_from_file(model_mtmt_mvp)

        # AND the mapping data
        mtmt_mapping = get_mapping_from_file(mapping_file)

        # THEN a MtmtMapping is returned with the expected trustzones
        mtmt_trustzone_parser = MTMTTrustzoneParser(mtmt, mtmt_mapping, diagram_representation.id)
        trustzones = mtmt_trustzone_parser.parse()

        assert len(trustzones) == 2
        trustzone = trustzones[0]
        assert trustzone.id == '75605184-4ca0-43be-ba4c-5fa5ad15e367'
        assert trustzone.name == 'Internet'
        assert trustzone.type == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9'
        trustzone = trustzones[1]
        assert trustzone.id == '24cdf4da-ac7f-4a35-bab0-29256d4169bf'
        assert trustzone.name == 'Private Secured Cloud'
        assert trustzone.type == '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'

    @mark.parametrize('mapping_file', [mtmt_default_mapping, mtmt_default_mapping_legacy, mtmt_default_mapping_no_type])
    def test_parse_default_trustzones(self, mapping_file):
        # GIVEN the Mtmt data
        mtmt = get_mtmt_from_file(test_resource_paths.mtmt_sdl_all_components)

        # AND the mapping data
        mtmt_mapping = get_mapping_from_file(mapping_file)

        # THEN a MtmtMapping is returned with the expected trustzones
        mtmt_trustzone_parser = MTMTTrustzoneParser(mtmt, mtmt_mapping, diagram_representation.id)
        trustzones = mtmt_trustzone_parser.parse()

        assert len(trustzones) == 2
        trustzone = trustzones[0]
        assert trustzone.id == '283137d7-a5f8-4433-a1e3-85cfce467eaf'
        assert trustzone.name == 'The Generic Trust Border Boundary'
        assert trustzone.type == '6376d53e-6461-412b-8e04-7b3fe2b397de'
        assert len(trustzone.representations) == 1
        representation: RepresentationElement = trustzone.representations[0]
        assert representation.id == '283137d7-a5f8-4433-a1e3-85cfce467eaf-representation'
        assert representation.name == 'The Generic Trust Border Boundary Representation'
        assert representation.position == {'x': 80, 'y': 32}
        assert representation.size == {'width': 539, 'height': 560}
        assert representation.representation == 'project-test-diagram'
        trustzone = trustzones[1]
        assert trustzone.id == '2d580de4-73e2-4dc7-8b77-d4ac347454a3'
        assert trustzone.name == 'The CorpNet Trust Boundary'
        assert trustzone.type == '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'
        assert len(trustzone.representations) == 1
        representation: RepresentationElement = trustzone.representations[0]
        assert representation.id == '2d580de4-73e2-4dc7-8b77-d4ac347454a3-representation'
        assert representation.name == 'The CorpNet Trust Boundary Representation'
        assert representation.position == {'x': 725, 'y': 62}
        assert representation.size == {'height': 451, 'width': 567}
        assert representation.representation == 'project-test-diagram'

    @mark.parametrize('mapping_file', [mtmt_default_mapping, mtmt_default_mapping_legacy, mtmt_default_mapping_no_type])
    def test_parse_unmapped_trustzones(self, mapping_file):
        # GIVEN the Mtmt data with one trustzone
        mtmt = get_mtmt_from_file(test_resource_paths.mtmt_unmapped_trustzone)

        # AND the mapping data without the mapping of the trustzone
        mtmt_mapping = get_mapping_from_file(mapping_file)

        # THEN a MtmtMapping is returned with the default trustzone
        parser = MTMTTrustzoneParser(mtmt, mtmt_mapping, diagram_representation.id)
        trustzones = parser.parse()

        assert len(trustzones) == 1
        trustzone = trustzones[0]
        assert trustzone.id == '128499a2-a137-450a-be99-c8ee519a66d6'
        assert trustzone.name == 'Internet Explorer Boundaries'
        assert trustzone.type == 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
        assert len(trustzone.representations) == 1
        representation: RepresentationElement = trustzone.representations[0]
        assert representation.id == '128499a2-a137-450a-be99-c8ee519a66d6-representation'
        assert representation.name == 'Internet Explorer Boundaries Representation'
        assert representation.position == {'x': 487, 'y': 274}
        assert representation.size == {'height': 277, 'width': 397}
        assert representation.representation == 'project-test-diagram'

    def test_nested_trust_zones(self):
        # GIVEN the provider loader
        mtmt = get_mtmt_from_file(nested_trustzones_tm7)

        # AND a valid MTMT mapping file
        mtmt_mapping = get_mapping_from_file(mtmt_default_mapping)

        # WHEN we parse the trust zones
        parser = MTMTTrustzoneParser(mtmt, mtmt_mapping, diagram_representation.id)
        trustzones = parser.parse()

        # THEN we check the trust zones parents
        assert len(trustzones) == 3
        current = trustzones[0]
        assert current.id == '351f4038-244d-4de5-bfa0-00c17f2a1fa2'
        assert not current.parent
        assert not current.parent_type
        current = trustzones[1]
        assert current.id == '9cbb5581-99cc-463b-a77a-c0dcae3b96d7'
        assert current.parent == '351f4038-244d-4de5-bfa0-00c17f2a1fa2'
        assert current.parent_type == 'trustZone'
        current = trustzones[2]
        assert current.id == '26e6fdb8-013f-4d59-bb11-208eec4d6bc9'
        assert not current.parent
        assert not current.parent_type
