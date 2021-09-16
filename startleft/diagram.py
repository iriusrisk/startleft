import logging
logger = logging.getLogger(__name__)

import math
from lxml import etree
from deepmerge import always_merger

class Cell:
    def merge_styles(self):
        self.style_map["ir.ref"] = self.data["id"]      
        if "properties" in self.data:
            if "style" in self.data["properties"]:
              for k,v in self.data["properties"]["style"].items():
                if v:
                    self.style_map[k] = v
                else:
                    self.style_map.pop(k, None)
            for k, v in self.ir_map.items():
                if v:
                    self.style_map[k] = v
                else:
                    self.style_map.pop(k, None)
            for k in self.ir_map.keys():
                if k in self.data["properties"]:
                    if self.data["properties"][k]:
                        self.style_map[k] = self.data["properties"][k]
                    else:
                        self.style_map.pop(k, None)
        return ";".join("{}={}".format(k, v) for k, v in self.style_map.items())+";"

    def merge_properties(self, maps):
        map_found = False    
  
        if not "properties" in self.data:
            self.data["properties"] = {}        
        for map in maps:
            if map["type"] == self.data["type"]:
                map_found = True
                always_merger.merge(self.data["properties"], map["properties"])
        if not map_found:
            for map in maps:
                if map["type"] == "default":
                    always_merger.merge(self.data["properties"], map["properties"])

    def to_cell(self):
        return {
            "data": self.data,
            "style": self.merge_styles()
        }


class Trustzone(Cell):
    def __init__(self, trustzone):
        self.ir_map = {
            "ir.type":  "TRUSTZONE",
            "ir.ref": ""
        }
        self.style_map = {
            "editable": "0",
            "recursiveResize": "0",
            "rounded": "0",
            "whiteSpace": "wrap",
            "html": "1",
            "dashed": "1",
            "strokeColor": "#FF3332",
            "verticalAlign": "top",
            "strokeWidth": "2",
            "fillColor": "#F5F5F5",
            "fontColor": "#000000",
            "opacity": "60",
            "connectable": "0",
            "container": "1"
        }
        self.data = trustzone


class Component(Cell):
    def __init__(self, component):
        self.ir_map = {
            "ir.type": "COMPONENT",
            "ir.synchronized": "1",
            "ir.componentDefinition.ref": "empty-component",
            "ir.tags": ""
        }
        self.style_map = {
            "outlineConnect": "0",
            "gradientColor": "#F78E04",
            "gradientDirection": "north",
            "fillColor": "#D05C17",
            "strokeColor": "#ffffff",
            "dashed": "0",
            "verticalLabelPosition": "bottom",
            "verticalAlign": "top",
            "align": "center",
            "fontStyle": "0",
            "aspect": "fixed",
            "rounded": "1",
            "whiteSpace": "wrap",
            "html": "1",
            "strokeWidth": "3",
            "fontColor": "#064C79",
            "fontSize": "12",
            "shape": "mxgraph.aws4.resourceIcon"
        }
        self.data = component

class Dataflow(Cell):
    def __init__(self, dataflow):
        self.ir_map = {
            "ir.synchronized": "1",
            "ir.ref": ""
        }
        self.style_map = {
            "edgeStyle": "none",
            "curved": "1",
            "html": "1",
            "strokeColor": "#27aae1",
            "strokeWidth": "3"
        }
        self.data = dataflow

class Diagram:
    def __init__(self):
        self.map = {}
        self.width = 1468
        self.height = 733
        self.tz_delta = 50
        self.component_width = 64
        self.component_height = 64
        self.component_space_x = 256
        self.component_space_y = 256
        self.default_node_size = 100

        self.file = etree.Element("mxfile", host="fraser.iriusrisk.com", modified="2021-06-17T09:59:40.298Z", agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36", version="12.2.4", etag="yWk9nYPBV6YaXUT6rb4Y", pages="1")
        diagram = etree.SubElement(self.file, "diagram", id="u3LjUtK0nmesnV5ISQRV", name="Page-1")
        graph = etree.SubElement(diagram, "mxGraphModel", dx=str(self.width), dy=str(self.height), grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="4681", pageHeight="3300", math="0", shadow="0")
        self.root = etree.SubElement(graph, "root")
        etree.SubElement(self.root, "mxCell", id="0")
        etree.SubElement(self.root, "mxCell", id="1", parent="0")

    def load_map(self, map):
        always_merger.merge(self.map, map)

    def add_trustzone(self, trustzone):
        tz = Trustzone(trustzone)
        tz.ir_map["ir.ref"] = tz.data["id"]
        tz.merge_properties(self.map["trustzones"])

        tz_cell = tz.to_cell()
        cell = etree.SubElement(self.root, "mxCell", id=tz_cell["data"]["id"], value=tz_cell["data"]["name"], style=tz_cell["style"], parent="1", vertex="1")
        tzgeo = etree.SubElement(cell, "mxGeometry",  x="750", y="160", width="180", height="230")
        tzgeo.attrib["as"] = "geometry"

    def add_component(self, component):
        c = Component(component)
        c.ir_map["ir.tags"] = ",".join(c.data['tags'])
        c.merge_properties(self.map["components"])

        c_cell = c.to_cell()        
        cell = etree.SubElement(self.root, "mxCell", id=c_cell["data"]["id"], value=c_cell["data"]["name"], style=c_cell["style"], parent=c_cell["data"]["parent"], vertex="1")
        cgeo = etree.SubElement(cell, "mxGeometry")

        if "width" in c_cell["data"]["properties"]:
            cgeo.attrib["width"] = str(c_cell["data"]["properties"]["width"])
        else:
            cgeo.attrib["width"] = str(self.component_width)
        if "height" in c_cell["data"]["properties"]:
            cgeo.attrib["height"] = str(c_cell["data"]["properties"]["height"])
        else:
            cgeo.attrib["height"] = str(self.component_height)

        cgeo.attrib["as"] = "geometry"

    def add_dataflow(self, dataflow):
        d = Dataflow(dataflow)
        d.ir_map["ir.ref"] = d.data["id"]
        d.merge_properties(self.map["dataflows"])

        d_cell = d.to_cell()
        cell = etree.SubElement(self.root, "mxCell", id=d_cell["data"]["id"], value=d_cell["data"]["name"], style=d_cell["style"], parent="1", source=d_cell["data"]["from"], target=d_cell["data"]["to"], edge="1")
        cgeo = etree.SubElement(cell, "mxGeometry")
        cgeo.attrib["as"] = "geometry"
        cgeo.attrib["relative"] = "1"

    def build_tree(self):
        list_child_parent = []
        for child in self.root:
            if not "parent" in child.attrib:
                continue

            if "edge" in child.attrib:
                continue # skip dataflows

            list_child_parent.append((child.attrib["id"], child.attrib["parent"]))

        has_parent = set()
        all_items = {}
        for child, parent in list_child_parent:
            if parent not in all_items:
                all_items[parent] = {}
            if child not in all_items:
                all_items[child] = {}
            all_items[parent][child] = all_items[child]
            has_parent.add(child)

        result = {}
        for key, value in all_items.items():
            if key not in has_parent:
                result[key] = value
        return result

    def traverse_to_layers(self, tree, layers, layer_index):
        if not layer_index in layers:
            layers[layer_index] = []
        
        for parent, children in tree.items():
            layers[layer_index].append({"parent": parent, "children": list(children.keys())})
            self.traverse_to_layers(children, layers, layer_index+1)

    def generate_layout(self):
        tree = self.build_tree()

        layers = {}
        self.traverse_to_layers(tree, layers, 0)
        deepest_layer = max(layers.keys())

        for layer_index in range(deepest_layer, 0, -1):
            for node_obj in layers[layer_index]:
                node = self.root.find(".//mxCell[@id='{}']".format(node_obj["parent"]))
                nodegeo = node[0] if len(node) > 0 else None

                num_children = len(node_obj["children"])
                if num_children > 0:
                    # Add size to components with children
                    child_widths = []
                    for child_id in node_obj["children"]:
                        child = self.root.find(".//mxCell[@id='{}']".format(child_id))
                        childgeo = child[0]
                        child_widths.append(int(childgeo.attrib["width"]))

                    max_child_size = max(child_widths)
                    max_columns_number = math.ceil(math.sqrt(num_children))

                    row = 0
                    col = 0
                    max_component_x = 0
                    max_component_y = 0
                    for child_id in node_obj["children"]:
                        child = self.root.find(".//mxCell[@id='{}']".format(child_id))
                        childgeo = child[0]
                        # Sets the position of the elements using a grid distribution
                        child_x = self.tz_delta + (col * (self.tz_delta + max_child_size))
                        child_y = self.tz_delta + (row * (self.tz_delta + max_child_size))
                        childgeo.attrib["x"] = str(child_x)
                        childgeo.attrib["y"] = str(child_y)

                        # Set the size of the parent component by looking the last x and y position of its children
                        component_x = int(childgeo.attrib['x']) + int(childgeo.attrib['width'])
                        component_y = int(childgeo.attrib['y']) + int(childgeo.attrib['height'])
                        max_component_x = max(component_x, max_component_x)
                        max_component_y = max(component_y, max_component_y)

                        col += 1

                        if col >= max_columns_number:
                            col = 0
                            row += 1

                    if nodegeo is not None:
                        nodegeo.attrib["width"] = str(max_component_x + self.tz_delta)
                        nodegeo.attrib["height"] = str(max_component_y + self.tz_delta)

                else:
                    # Add size to components without children
                    if nodegeo is not None:
                        nodegeo.attrib["width"] = str(self.default_node_size)
                        nodegeo.attrib["height"] = str(self.default_node_size)

    def xml(self):
        return etree.tostring(self.file, pretty_print=True, xml_declaration=True, encoding='utf-8', method='xml')