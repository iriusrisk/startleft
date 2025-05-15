import pytest
from typing import Optional

from slp_drawio.slp_drawio.load.stencil_extractors import (
    MxCell,
    register_extractor,
    extract_stencil_type,
    _extractors,
)


@pytest.fixture
def clear_registry():
    _extractors.clear()

# --- Registry structural integrity test ---

def test_all_registered_extractors_are_callable():
    assert len(_extractors) == 2
    for extractor in _extractors:
        assert callable(extractor)


# --- extract_stencil_type behavior tests ---

def test_extract_stencil_type_calls_first_matching_extractor(clear_registry):
    called = []

    @register_extractor
    def extractor1(_: MxCell) -> Optional[str]:
        called.append("1")
        return None

    @register_extractor
    def extractor2(_: MxCell) -> Optional[str]:
        called.append("2")
        return "azure.vm"

    result = extract_stencil_type({"style": "irrelevant"})

    assert result == "azure.vm"
    assert called == ["1", "2"]


def test_extract_stencil_type_returns_none_if_no_extractors_match(clear_registry):
    @register_extractor
    def extractor(_: MxCell) -> Optional[str]:
        return None

    result = extract_stencil_type({"style": "none"})
    assert result is None

