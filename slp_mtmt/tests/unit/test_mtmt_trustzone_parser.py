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
        assert trustzone.id == '75605184-4ca0-43be-ba4c-5fa5ad15e367'
        assert trustzone.name == 'Internet'
        assert trustzone.type == 'internet'
        trustzone = trustzones[1]
        assert trustzone.id == '24cdf4da-ac7f-4a35-bab0-29256d4169bf'
        assert trustzone.name == 'Private Secured Cloud'
        assert trustzone.type == 'private-secured'

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
        assert trustzone.id == '283137d7-a5f8-4433-a1e3-85cfce467eaf'
        assert trustzone.name == 'The Generic Trust Border Boundary'
        assert trustzone.type == 'public'
        trustzone = trustzones[1]
        assert trustzone.id == '2d580de4-73e2-4dc7-8b77-d4ac347454a3'
        assert trustzone.name == 'The CorpNet Trust Boundary'
        assert trustzone.type == 'private-secured'


    def test_parse_unmapped_trustzones(self):
        # GIVEN the Mtmt data with one trustzone
        mtmt = get_mtmt_from_file(test_resource_paths.mtmt_unmapped_trustzone)

        # AND the mapping data without the mapping of the trustzone
        mtmt_mapping = get_mapping_from_file(test_resource_paths.mtmt_default_mapping)

        # THEN a MtmtMapping is returned with the default trustzone
        parser = MTMTTrustzoneParser(mtmt, mtmt_mapping)
        trustzones = parser.parse()

        assert len(trustzones) == 1
        trustzone = trustzones[0]
        assert trustzone.id == '128499a2-a137-450a-be99-c8ee519a66d6'
        assert trustzone.name == 'Internet Explorer Boundaries'
        assert trustzone.type == 'public-cloud'

