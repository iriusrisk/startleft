import pytest
from pytest import mark, param

from sl_util.sl_util import secure_regex as re
from sl_util.sl_util.file_utils import get_byte_data
from sl_util.tests.util.file_utils import generate_temporary_file
from slp_base import MappingFileNotValidError
from slp_base.slp_base.errors import ErrorCode
from slp_base.slp_base.mapping import MAX_SIZE as MAPPING_MAX_SIZE, MIN_SIZE as MAPPING_MIN_SIZE
from slp_drawio import DrawioProcessor
from slp_drawio.tests.resources import test_resource_paths
from slp_drawio.tests.resources.test_resource_paths import shape_names_with_html, default_drawio_mapping

SAMPLE_ID = 'id'
SAMPLE_NAME = 'name'
SAMPLE_VALID_DRAWIO_PATH = test_resource_paths.aws_minimal_xml
DEFAULT_MAPPING_FILE = get_byte_data(test_resource_paths.default_drawio_mapping)


class TestDrawioProcessor:
    @mark.parametrize('mappings', [
        param([generate_temporary_file(MAPPING_MIN_SIZE - 1).file.read(), DEFAULT_MAPPING_FILE], id='mapping file too small'),
        param([generate_temporary_file(MAPPING_MAX_SIZE + 1).file.read(), DEFAULT_MAPPING_FILE], id='mapping file too big'),
        param([DEFAULT_MAPPING_FILE, generate_temporary_file(MAPPING_MIN_SIZE - 1).file.read()], id='custom mapping file too small'),
        param([DEFAULT_MAPPING_FILE, generate_temporary_file(MAPPING_MAX_SIZE + 1).file.read()], id='custom mapping file too big')
    ])
    def test_invalid_mapping_size(self, mappings: list[bytes]):
        # GIVEN a valid drawio
        drawio_file = open(SAMPLE_VALID_DRAWIO_PATH, 'rb')

        # AND a mapping file with an invalid size ('mappings' arg)

        # WHEN DrawioProcessor::process is invoked
        # THEN a MappingFileNotValidError is raised
        with pytest.raises(MappingFileNotValidError) as error:
            DrawioProcessor(SAMPLE_ID, SAMPLE_NAME, drawio_file, mappings).process()

        # AND the error details are correct
        assert ErrorCode.MAPPING_FILE_NOT_VALID == error.value.error_code
        assert 'Mapping files are not valid' == error.value.title
        assert 'Mapping files are not valid. Invalid size' == error.value.detail
        assert 'Mapping files are not valid. Invalid size' == error.value.message

    @pytest.mark.parametrize('filepath', [
        pytest.param(shape_names_with_html, id='aws_with_html'),
    ])
    def test_handle_html_shape_names(self, filepath: str):
        # GIVEN the valid file
        file = open(filepath, 'rb')
        # AND the default mapping
        default_drawio_mapping_file = get_byte_data(default_drawio_mapping)

        # AND the processor
        processor = DrawioProcessor('html_names', 'HTML Names', file, [default_drawio_mapping_file])

        # WHEN we process the file
        result = processor.process()

        # THEN the component names are correctly parsed
        components = result.components
        components.sort(key=lambda c: c.name)
        assert len(components) == 10
        assert components[0].name == 'Bold EC2'
        assert components[1].name == 'Combined EC2'
        assert components[2].name == 'Courier EC2'
        assert components[3].name == 'Drawio example with Cell names with HTML'
        assert components[4].name == 'Font size 16 EC2'
        assert components[5].name == 'Italic EC2'
        assert components[6].name == 'Non HTML EC2'
        assert components[7].name == 'Red EC2'
        assert components[8].name == 'Strikethrough EC2'
        assert components[9].name == 'Underline EC2'

        # AND the representation attributes has the style from the html original name
        assert 'fontStyle=1;' in components[0].representations[0].attributes['style']
        c1 = components[1].representations[0].attributes['style']
        assert _validate_font_styles(c1, '0', '15')
        assert 'fontFamily=Courier New;' in c1
        assert 'fontColor=#ff0000;' in c1
        assert 'fontFamily=Courier New;' in components[2].representations[0].attributes['style']
        assert 'fontSize=16;' in components[4].representations[0].attributes['style']
        c5 = components[5].representations[0].attributes['style']
        assert _validate_font_styles(c5, '0', '2')
        assert 'fontStyle=0;' in components[6].representations[0].attributes['style']
        assert 'fontColor=#ff0000;' in components[7].representations[0].attributes['style']
        assert _validate_font_styles(components[8].representations[0].attributes['style'], '0', '8')
        assert _validate_font_styles(components[9].representations[0].attributes['style'], '0', '4')


def _validate_font_styles(style: str, value1: str, value2: str) -> bool:
    """
    Returns true if in the given style string there are exactly two fontStyle
    definitions (value1 then value2), with none before, between, or after.
    """
    m = re.search(fr"(.*)fontStyle\s*=\s*{value1}(.*)?fontStyle\s*=\s*{value2}(.*)", style)
    return m and "fontStyle" not in m.group(1) and "fontStyle" not in m.group(2) and "fontStyle" not in m.group(3)
