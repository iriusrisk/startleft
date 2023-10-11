from collections import defaultdict

from defusedxml import ElementTree


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


def add_attributes(d, t, tag_name):
    d[tag_name].update(get_attrs(t.attrib))


def add_text(children, d, t, tag_name):
    text = t.text.strip()
    if children or t.attrib:
        if text:
            d[tag_name]['text'] = text
    else:
        d[tag_name] = text


def add_children(children, tag_name, separated_attributes):
    dd = defaultdict(list)
    for dc in [xml2dict(ch, separated_attributes) for ch in children]:
        for k, v in dc.items():
            dd[k].append(v)
    return {tag_name: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}


def xml2dict(t, separated_attributes=False):
    tag_name = get_tag(t)
    d = {tag_name: {} if t.attrib else None}
    children = list(t)
    if children:
        d = add_children(children, tag_name, separated_attributes=separated_attributes)
    if t.text:
        add_text(children, d, t, tag_name)

    if t.attrib:
        if separated_attributes:
            d['attrib'] = get_attrs(t.attrib)
        else:
            add_attributes(d, t, tag_name)

    return d


class XmlToJson:

    def __init__(self, xml: str):
        self.xml = xml

    def to_json(self):
        xml_data = ElementTree.XML(self.xml)
        return xml2dict(xml_data)
