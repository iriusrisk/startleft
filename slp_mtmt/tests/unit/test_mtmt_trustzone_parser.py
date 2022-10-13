from slp_mtmt.slp_mtmt.parse.mtmt_trustzone_parser import MTMTTrustzoneParser
from slp_mtmt.tests.mtmt_test_utils import get_mtmt_from_file, get_mapping_from_file
from slp_mtmt.tests.resources import test_resource_paths


class TestMTMTTrustzoneParser:

    def test_parse_with_empty_mapping_file(self):
        # GIVEN the Mtmt data
        mtmt = get_mtmt_from_file(test_resource_paths.model_mtmt_mvp)

        # AND the mapping data
        mtmt_mapping = get_mapping_from_file(test_resource_paths.mtmt_empty_mapping_file)

        # THEN a MtmtMapping is returned with no trustzones
        mtmt_trustzone_parser = MTMTTrustzoneParser(mtmt, mtmt_mapping)
        trustzones = mtmt_trustzone_parser.parse()

        assert len(trustzones) == 0

    def test_parse_with_filled_mapping_file(self):
        # GIVEN the Mtmt data
        mtmt = get_mtmt_from_file(test_resource_paths.model_mtmt_mvp)

        # AND the mapping data
        mtmt_mapping = get_mapping_from_file(test_resource_paths.mapping_mtmt_mvp)

        # THEN a MtmtMapping is returned with the expected trustzones
        mtmt_trustzone_parser = MTMTTrustzoneParser(mtmt, mtmt_mapping)
        trustzones = mtmt_trustzone_parser.parse()

        assert len(trustzones) == 2
        trustzone = trustzones[0]
        assert trustzone.id == 'f0ba7722-39b6-4c81-8290-a30a248bb8d9'
        assert trustzone.name == 'Internet'
        trustzone = trustzones[1]
        assert trustzone.id == '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'
        assert trustzone.name == 'Private Secured Cloud'

    def test_parse_default_trustzones(self):
        # GIVEN the Mtmt data
        mtmt = get_mtmt_from_file(test_resource_paths.mtmt_sdl_all_components)

        # AND the mapping data
        mtmt_mapping = get_mapping_from_file(test_resource_paths.mtmt_default_mapping)

        # THEN a MtmtMapping is returned with the expected trustzones
        mtmt_trustzone_parser = MTMTTrustzoneParser(mtmt, mtmt_mapping)
        trustzones = mtmt_trustzone_parser.parse()

        assert len(trustzones) == 2
        trustzone = trustzones[0]
        assert trustzone.id == '6376d53e-6461-412b-8e04-7b3fe2b397de'
        assert trustzone.name == 'The Generic Trust Border Boundary'
        trustzone = trustzones[1]
        assert trustzone.id == '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'
        assert trustzone.name == 'The CorpNet Trust Boundary'
