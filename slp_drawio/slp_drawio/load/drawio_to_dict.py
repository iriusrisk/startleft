import base64
import logging
import zlib
from tempfile import SpooledTemporaryFile
from typing import List
from urllib.parse import unquote

from defusedxml import ElementTree

from sl_util.sl_util.xml_to_dict import XmlToDict

logger = logging.getLogger(__name__)

DEFAULT_ENCODING = 'utf8'


def __is_diagram_encoded(diagram_tags: List) -> bool:
    return len(diagram_tags) <= 1


def _decode_diagram(content: str) -> str:
    tree = ElementTree.XML(content)
    tree_tag = tree.find('diagram')
    if __is_diagram_encoded(list(tree_tag.iter())):
        data = base64.b64decode(tree_tag.text, validate=True)
        xml = zlib.decompress(data, wbits=-15).decode()
        xml = unquote(xml)
        diagram_tree = ElementTree.fromstring(xml)
        tree_tag.append(diagram_tree)
        tree_tag.text = None
        return ElementTree.tostring(tree, encoding=DEFAULT_ENCODING)


def _get_file_content(source: SpooledTemporaryFile) -> str:
    content = source.read()
    if content:
        return content.decode(encoding=DEFAULT_ENCODING)


class DrawIOToDict:

    def __init__(self, source):
        self.source = source

    def to_dict(self) -> dict:
        content = _get_file_content(self.source.file)
        if not content:
            return {}

        diagram = _decode_diagram(content) or content

        return XmlToDict(diagram).to_dict()
