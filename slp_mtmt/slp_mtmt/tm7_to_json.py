from collections import defaultdict

from defusedxml import ElementTree as ET


def get_attrs(attrs):
    result = {}
    if attrs is not None:
        for key, value in attrs.items():
            result[remove_curly_info(key)] = value
    return result


def get_tag(t):
    return remove_curly_info(t.tag)


def remove_curly_info(value):
    if '}' in value:
        return value.split('}')[1]
    else:
        return value


def xml2dict(t):
    d = {get_tag(t): {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(xml2dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {get_tag(t): {k: v[0] if len(v) == 1 else v
                          for k, v in dd.items()}}
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[get_tag(t)]['text'] = text
        else:
            d[get_tag(t)] = text

    if t.attrib:
        d['attrib'] = get_attrs(t.attrib)
        
    return d


class Tm7ToJson:

    def __init__(self, xml: str):
        self.xml = xml

    def to_json(self):
        xml_data = ET.XML(self.xml)
        return xml2dict(xml_data)
