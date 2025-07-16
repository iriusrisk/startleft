import base64
import logging
import zlib
from typing import List
from urllib.parse import unquote

from defusedxml import ElementTree

from sl_util.sl_util.file_utils import read_byte_data
from sl_util.sl_util.xml_to_dict import XmlToDict

logger = logging.getLogger(__name__)

DEFAULT_ENCODING = 'utf8'


def __is_diagram_encoded(diagram_tags: List) -> bool:
    return len(diagram_tags) <= 1


def _decode_diagram(content: str) -> str | None:
    tree = ElementTree.XML(content)
    tree_tag = tree if tree.tag == 'mxGraphModel' else tree.find('diagram')
    if __is_diagram_encoded(list(tree_tag.iter())):
        data = base64.b64decode(tree_tag.text, validate=True)
        xml = zlib.decompress(data, wbits=-15).decode()
        xml = unquote(xml)
        diagram_tree = ElementTree.fromstring(xml)
        tree_tag.append(diagram_tree)
        tree_tag.text = None
        return ElementTree.tostring(tree, encoding=DEFAULT_ENCODING)


class DrawIOToDict:

    def __init__(self, source):
        self.source = source

    def to_dict(self) -> dict:
        content = read_byte_data(self.source)
        if not content:
            return {}

        diagram = _decode_diagram(content) or content

        return XmlToDict(diagram).to_dict()
