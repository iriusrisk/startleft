import base64
import zlib
from urllib.parse import unquote

from defusedxml import ElementTree

from sl_util.sl_util.xml_to_json import XmlToJson


class DrawioWrapper:

    def __init__(self, content: bytes):
        self.encoding = 'utf8'
        self.content: str = content.decode()
        self.decode_b64_tag('diagram')

    def json(self) -> dict:
        return XmlToJson(self.content).to_json()

    def decode_b64_tag(self, tag):
        tree = ElementTree.XML(self.content)
        tree_tag = tree.find(tag)
        children = list(tree_tag.iter())
        if len(children) <= 1:
            print(f'{tag} tag is encoded')
            data = base64.b64decode(tree_tag.text, validate=True)
            xml = zlib.decompress(data, wbits=-15).decode()
            xml = unquote(xml)
            diagram_tree = ElementTree.fromstring(xml)
            tree_tag.append(diagram_tree)
            tree_tag.text = None
            self.content = ElementTree.tostring(tree, encoding=self.encoding)
