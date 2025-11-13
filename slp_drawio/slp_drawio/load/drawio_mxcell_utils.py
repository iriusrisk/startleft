from typing import Optional

from sl_util.sl_util.str_utils import remove_html_tags_and_entities
from slp_drawio.slp_drawio.parse.drawio_styles_from_html_tags_parser import DrawioStylesFromHtmlTagsParser


def get_cell_style(mx_cell: dict) -> str:
    cell_value = mx_cell.get('value') or mx_cell.get('label')
    return str(mx_cell.get('style')) + _extract_css_from_cell_value(cell_value)


def get_cell_parent_id(mx_cell: dict, mx_cell_components: list[dict]):
    return mx_cell.get('parent') \
        if any(item.get('id') == mx_cell.get('parent') for item in mx_cell_components) else None


def get_cell_name(mx_cell: dict) -> Optional[str]:
    cell_value = mx_cell.get('value') or mx_cell.get('label')
    if cell_value:
        cell_value = remove_html_tags_and_entities(cell_value).strip()
        return cell_value if len(cell_value) > 1 else f'_{cell_value}'
    return None


def _extract_css_from_cell_value(html: Optional[str]) -> str:
    if not html:
        return ""
    parser = DrawioStylesFromHtmlTagsParser()
    css_str = ";".join(parser.parse(html))
    return f"{css_str};" if css_str else ""
