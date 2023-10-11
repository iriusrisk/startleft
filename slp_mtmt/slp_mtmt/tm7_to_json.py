from defusedxml import ElementTree as ET

from sl_util.sl_util.xml_to_json import xml2dict


class Tm7ToJson:

    def __init__(self, xml: str):
        self.xml = xml

    def to_json(self):
        xml_data = ET.XML(self.xml)
        return xml2dict(xml_data, separated_attributes=True)
