import sl_util.sl_util.secure_regex as re
from typing import Optional
from slp_drawio.slp_drawio.load.stencil_extractors import MxCell, register_extractor


def __extract_image_value(mx_cell: MxCell) -> Optional[str]:
    style = mx_cell.get("style", "")
    for part in style.split(";"):
        if part.startswith("image="):
            image_value = part[len("image="):]
            if not image_value.startswith("data:") and re.match(r"img/lib/azure\d*/", image_value):
                return image_value
    return None


@register_extractor
def extract_azure_type(mx_cell: MxCell) -> Optional[str]:
    """
    Extract an Azure image path from mx_cell if it matches a specific pattern.
    """
    image_path = __extract_image_value(mx_cell)
    return '/'.join(image_path.split('.')[-2].split('/')[-2:]) \
        if image_path and '.' in image_path and '/' in image_path \
        else None
