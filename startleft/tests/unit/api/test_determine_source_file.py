import unittest
from unittest.mock import MagicMock

from slp_base import MappingFileNotValidError
from startleft.startleft.api.controllers.iac.iac_create_otm_controller import _determine_source_file


class TestDetermineSourceFile(unittest.TestCase):
    def test_both_files_present(self):
        mapping_file = MagicMock()
        default_mapping_file = MagicMock()

        with self.assertRaises(MappingFileNotValidError) as context:
            _determine_source_file(mapping_file, default_mapping_file)

        self.assertIn("default_mapping_file and mapping_file cannot be present", str(context.exception.args))

    def test_no_files_present(self):
        with self.assertRaises(MappingFileNotValidError) as context:
            _determine_source_file(None, None)

        self.assertIn("Mapping file must not be void", str(context.exception.args))

    def test_mapping_file_present(self):
        mapping_file = MagicMock()
        mapping_file.file.__enter__.return_value.read.return_value = b"mapping data"

        result = _determine_source_file(mapping_file, None)
        self.assertEqual(result, [b"mapping data"])

    def test_default_mapping_file_present(self):
        default_mapping_file = MagicMock()
        default_mapping_file.file.__enter__.return_value.read.return_value = b"default mapping data"

        result = _determine_source_file(None, default_mapping_file)
        self.assertEqual(result, [b"default mapping data"])
