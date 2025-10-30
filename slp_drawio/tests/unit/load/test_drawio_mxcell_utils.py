from typing import Dict, List

import pytest

from slp_drawio.slp_drawio.load.drawio_mxcell_utils import get_cell_parent_id, get_cell_name
from slp_drawio.slp_drawio.load.drawio_mxcell_utils import get_cell_style


@pytest.mark.parametrize('mx_cell, components, expected', [
    pytest.param({}, [], None, id="with mxCell without parent None"),
    pytest.param({'parent': 1}, [{'id': 1}], 1, id="parent exists in components"),
    pytest.param({'parent': 1}, [{'id': 2}], None, id="parent not exists in components"),
])
def test_get_cell_parent_id(mx_cell: Dict, components: List, expected):
    # GIVEN a mx_cell
    # WHEN we get the parent id
    parent_id = get_cell_parent_id(mx_cell, components)

    # THEN the parent is as expected
    assert parent_id == expected


@pytest.mark.parametrize('mx_cell, expected', [
    pytest.param({}, None, id="with mxCell without value or label None"),
    pytest.param({'value': ''}, None, id="empty value None"),
    pytest.param({'label': ''}, None, id="empty label None"),
    pytest.param({'value': 'A'}, '_A', id="single character value"),
    pytest.param({'label': 'B'}, '_B', id="single character label"),
    pytest.param({'value': '  Test Value  '}, 'Test Value', id="trailing spaces in value"),
    pytest.param({'label': '  Test Value  '}, 'Test Value', id="trailing spaces in label"),
    pytest.param({'label': '<div>Bold <b>Label</b></div>'}, 'Bold Label', id="HTML label"),
    pytest.param({'value': '<div>Bold <b>Label</b></div>'}, 'Bold Label', id="HTML value"),
])
def test_get_cell_name(mx_cell: Dict, expected):
    # GIVEN a mx_cell
    # WHEN we get the cell name
    cell_name = get_cell_name(mx_cell)

    # THEN the cell name is as expected
    assert cell_name == expected


@pytest.mark.parametrize('cell_name, expected', [
    pytest.param('<b>Bold Text</b>',
                 'sketch=0;fontColor=originalFCfontSize=originalFSI;fontFamily=OriginalFF;fontStyle=1;', id="bold"),
    pytest.param('<i>Italic Text</i>',
                 'sketch=0;fontColor=originalFCfontSize=originalFSI;fontFamily=OriginalFF;fontStyle=2;', id="italic"),
    pytest.param('<u>Underlined Text</u>',
                 'sketch=0;fontColor=originalFCfontSize=originalFSI;fontFamily=OriginalFF;fontStyle=4;',
                 id="underline"),
    pytest.param('<font face="Arial" size="4" color="#fa09bc">Custom Font</font>',
                 'sketch=0;fontColor=#fa09bc;fontFamily=Arial;fontStyle=originalFST;',
                 id="all combined"),
    pytest.param('Plain Text',
                 'sketch=0;fontColor=originalFCfontSize=originalFSI;fontFamily=OriginalFF;fontStyle=originalFST;',
                 id="plain text with no HTML"),
    pytest.param('', 'sketch=0;fontColor=originalFCfontSize=originalFSI;fontFamily=OriginalFF;fontStyle=originalFST;',
                 id="empty string"),
    pytest.param(None, 'sketch=0;fontColor=originalFCfontSize=originalFSI;fontFamily=OriginalFF;fontStyle=originalFST;',
                 id="None value")
])
def test_get_cell_style(cell_name, expected):
    # GIVEN a default styles that will be overridden
    default_styles = 'sketch=0;fontColor=originalFCfontSize=originalFSI;fontFamily=OriginalFF;fontStyle=originalFST;'

    # AND a mx_cell with value with HTML
    value_mx_cell = {'value': cell_name, 'style': default_styles}

    # AND a mx_cell with label with HTML
    label_mx_cell = {'label': cell_name, 'style': default_styles}

    # WHEN we get the font styles
    value_font_styles = get_cell_style(value_mx_cell)
    label_font_styles = get_cell_style(label_mx_cell)

    # THEN the font styles are as expected
    assert value_font_styles == expected
    assert label_font_styles == expected
