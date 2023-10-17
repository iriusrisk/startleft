import base64
import logging
import zlib
from tempfile import SpooledTemporaryFile
from urllib.parse import unquote

from defusedxml import ElementTree

from sl_util.sl_util.xml_to_dict import XmlToDict

logger = logging.getLogger(__name__)

DEFAULT_ENCODING = 'utf8'
DIAGRAM_TAG = 'diagram'


class DrawIOToDict:

    def __init__(self, source):
        file: SpooledTemporaryFile = source.file
        self.encoding = 'utf8'
        self.content: str = file.read().decode()
        self.decode_b64_tag('diagram')

    def to_dict(self) -> dict:
        return XmlToDict(self.content).to_dict()

    def decode_b64_tag(self, tag):
        tree = ElementTree.XML(self.content)
        tree_tag = tree.find(tag)
        children = list(tree_tag.iter())
        if len(children) <= 1:
            logger.debug(f'{tag} tag is encoded')
            data = base64.b64decode(tree_tag.text, validate=True)
            xml = zlib.decompress(data, wbits=-15).decode()
            xml = unquote(xml)
            diagram_tree = ElementTree.fromstring(xml)
            tree_tag.append(diagram_tree)
            tree_tag.text = None
            self.content = ElementTree.tostring(tree, encoding=self.encoding)
            logger.debug(f'{tag} tag decoded successfully')
