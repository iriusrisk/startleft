import pytest

from slp_drawio.slp_drawio.parse.drawio_styles_from_html_tags_parser import DrawioStylesFromHtmlTagsParser

TEST_DRAWIO_FONT_SIZE_KEY = 'fontSize'
TEST_DRAWIO_FONT_STYLE_KEY = 'fontStyle'
TEST_DRAWIO_FONT_COLOR_KEY = 'fontColor'
TEST_DRAWIO_FONT_FAMILY_KEY = 'fontFamily'


@pytest.mark.parametrize('html,expected', [
    pytest.param('<b>Bold text</b>', [f'{TEST_DRAWIO_FONT_STYLE_KEY}=1'], id="bold"),
    pytest.param('<i>Italic Text</i>', [f'{TEST_DRAWIO_FONT_STYLE_KEY}=2'], id="italic"),
    pytest.param('<u>Underlined Text</u>', [f'{TEST_DRAWIO_FONT_STYLE_KEY}=4'], id="underline"),
    pytest.param('<s>Strikethrough Text</s>', [f'{TEST_DRAWIO_FONT_STYLE_KEY}=8'], id="Strikethrough"),
    pytest.param('<b><i>Combined Text</i></b>', [f'{TEST_DRAWIO_FONT_STYLE_KEY}=3'], id="bold + italic"),
    pytest.param('<b><i><u>Combined Text</u></i></b>', [f'{TEST_DRAWIO_FONT_STYLE_KEY}=7'],
                 id="bold + italic + underline"),
    pytest.param('<b><i><u><s>Combined Text</s></u></i></b>', [f'{TEST_DRAWIO_FONT_STYLE_KEY}=15'],
                 id="bold + italic + underline + strikethrough"),
    pytest.param('<font face="Courier" size="4" color="#fb08cb">Custom Font</font>',
                 [f'{TEST_DRAWIO_FONT_COLOR_KEY}=#fb08cb', f'{TEST_DRAWIO_FONT_FAMILY_KEY}=Courier'],
                 id="font color, face and size"),
    pytest.param('<font face="Courier" size="4" color="#ffdd00">'
                 '<a href="https://example.com"><b><i><u>EC2 with HTML</b></i></u></a></font>',
                 [f'{TEST_DRAWIO_FONT_STYLE_KEY}=7', f'{TEST_DRAWIO_FONT_COLOR_KEY}=#ffdd00',
                  f'{TEST_DRAWIO_FONT_FAMILY_KEY}=Courier'], id="all styles combined"),

    pytest.param('Plain Text', [], id="plain text with no HTML"),
    pytest.param('', [], id="empty string")
])
def test_parse_style(html, expected):
    # GIVEN the parser
    parser = DrawioStylesFromHtmlTagsParser()
    # WHEN OldHTMLStyleParser::parse is called
    result = parser.parse(html)
    # THEN the style is correctly parsed
    assert result == expected
