from typing import Optional

from sl_util.sl_util.str_utils import remove_html_tags_and_entities
from slp_drawio.slp_drawio.parse.drawio_styles_from_html_tags_parser import DrawioStylesFromHtmlTagsParser


def get_cell_style(mx_cell: dict) -> str:
    cell_value = mx_cell.get('value') or mx_cell.get('label')
    return _join_styles(_extract_css_from_cell_value(cell_value), str(mx_cell.get('style')))


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
    return "; ".join(parser.parse(html)) + ";"


def _join_styles(style_a: str, style_b: str) -> str:
    """
    Joins two style strings, giving precedence to the first one in case of duplicate keys.
    :param style_a: The primary style string (e.g., from the cell value's HTML).
    :param style_b: The secondary style string (e.g., from the cell's style attribute).
    :return: A merged style string.
    """

    def to_dict(style_str: str) -> dict:
        if not style_str:
            return {}

        # Normalize separators
        style_str = style_str.replace(':', '=')

        # Split by semicolon and filter out empty parts.
        pairs = [pair.strip() for pair in style_str.split(';') if pair.strip()]

        style_dict = {}
        for pair in pairs:
            if '=' in pair:
                key, value = pair.split('=', 1)
                style_dict[key.strip()] = value.strip()
        return style_dict

    # The second dictionary's values are overwritten by the first one's in case of common keys.
    style_attribute_dict = to_dict(style_b)
    style_value_dict = to_dict(style_a)

    merged_styles = {**style_attribute_dict, **style_value_dict}

    return ';'.join([f'{key}={value}' for key, value in merged_styles.items() if value]) + ';'
