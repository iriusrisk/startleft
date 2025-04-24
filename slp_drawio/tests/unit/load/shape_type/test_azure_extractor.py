import pytest
from slp_drawio.slp_drawio.load.stencil_extractors.azure_extractor import extract_azure_type


# --- Extractor function tests ---

@pytest.mark.parametrize("style, expected", [
    ("image;image=img/lib/azure3/path.svg;", "azure3/path"),
    ("image;image=img/lib/azure/network/firewall.svg;", "network/firewall"),
])
def test_extract_azure_type_returns_expected_string(style, expected):
    mx_cell = {"style": style}
    result = extract_azure_type(mx_cell)
    assert result == expected


@pytest.mark.parametrize("style", [
    "image;image=img/lib/gcp/path.svg;",
    "image;image=data:image/svg+xml;base64,XYZ",
    "rounded=1;"
])
def test_extract_azure_type_returns_none_when_not_matched(style):
    mx_cell = {"style": style}
    assert extract_azure_type(mx_cell) is None
