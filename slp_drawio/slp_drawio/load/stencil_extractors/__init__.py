import importlib
import os
from typing import Any, Optional, Callable


MxCell = dict[str, Any]
MxCellTypeExtractor = Callable[[MxCell], Optional[str]]

_extractors: list[MxCellTypeExtractor] = []

def register_extractor(extract_fn: MxCellTypeExtractor):
    _extractors.append(extract_fn)
    return extract_fn

def extract_stencil_type(mx_cell: MxCell) -> Optional[str]:
    for extractor in _extractors:
        if shape_type := extractor(mx_cell):
            return shape_type
    return None

# Auto-discover all sibling modules
current_dir = os.path.dirname(__file__)
modules = [
    os.path.splitext(f)[0]
    for f in os.listdir(current_dir)
    if f.endswith(".py") and f not in ["__init__.py", "__pycache__"]
]

for module in modules:
    importlib.import_module(f".{module}", __package__)
