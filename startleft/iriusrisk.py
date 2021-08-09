import logging
logger = logging.getLogger(__name__)

from lxml import etree
from deepmerge import always_merger
import pkg_resources
import requests
import base64
import os
import yaml
from startleft.schema import Schema

class IriusTokenError(Exception):
    pass

class IriusServerError(Exception):
    pass

class IriusRisk:
    API_PATH = '/api/v1'

    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token
        self.name = None
        self.id = None
        self.map = {}
        self.otm = {}
        self.schema = {}

        self.dataflows = []
        self.trustzones = []
        self.components = []

    def headers(self):
        if not self.token:
            raise IriusTokenError        
        return {"api-token" : "{}".format(self.token)}

    def irius_url(self, path):
        if not self.base_url:
            raise IriusServerError
        return self.base_url + IriusRisk.API_PATH + path

    def load_otm_file(self, data):
        always_merger.merge(self.otm, data)

    def set_project(self):
        if not self.name:
            self.name = self.otm["project"]["name"]
        if not self.id:
            self.id = self.otm["project"]["id"]

    def load_map(self, map):
        for component in map["components"]:
            self.map[component["type"]] = component["properties"]["ir.componentDefinition.ref"]

    def add_dataflow(self, dataflow):
        self.dataflows.append(dataflow)

    def add_trustzone(self, trustzone):
        self.trustzones.append(trustzone)

    def add_component(self, component):
        if component["type"] in self.map:
            component["component_definition"] = self.map[component["type"]]
        else:
            component["component_definition"] = "empty-component"
        self.components.append(component)

    def find_trustzone(self, element):
        if "parent" in element:
            parent_id = element["parent"]

            if parent_id not in self.parent_tree:
                print(f"Unknown parent: {parent_id}")
                return
            parent = self.parent_tree[parent_id]
            if parent["type"] == "trustzone":
                return parent_id
            else:
                return self.find_trustzone(parent["component"])
        
    def resolve_component_trustzones(self):
        self.parent_tree = {}
        for trustzone in self.trustzones:
            id = trustzone["id"]
            self.parent_tree[id] = {
                "type": "trustzone",
                "trustzone": trustzone
            }
        for component in self.components:
            id = component["id"]
            self.parent_tree[id] = {
                "type": "component",
                "component": component
            }
        
        for component in self.components:
            component["trustzone"] = self.find_trustzone(component)

    def product_exists(self):
        url = self.irius_url("/products")
        response = requests.get(url, headers=self.headers())
        logger.debug(f"Response received {response.status_code}: {response.text}")
        for product in response.json():
            if product["ref"] == self.id:
                return True
        return False

    def update_product(self, diagram):
        product_xml = self.create_product_xml(diagram, draft="true")

        url = self.irius_rul(f"/products/upload/{self.id}")
        headers = self.headers()
        logger.debug("Writing product XML to 'product.xml'")
        with open("product.xml", "wb") as f:
            f.write(product_xml)
        logger.debug("Submitting updated product to IriusRisk")
        response = requests.post(url, files={"fileName": open("product.xml", "r")}, headers=headers)
        logger.debug(f"Response received {response.status_code}: {response.text}")
        response.close()

    def delete_product(self):
        url = self.irius_url(f"/products/{self.id}")
        headers = self.headers()
        logger.debug("Deleting product")
        response = requests.delete(url, headers=headers)
        logger.debug(f"Response received {response.status_code}: {response.text}")
        response.close()

    def create_product(self, diagram):
        product_xml = self.create_product_xml(diagram)

        url = self.irius_url("/products/upload/")
        data = {"ref": self.id, "name": self.name, "type": "STANDARD"}
        headers = self.headers()
        logger.debug("Writing product XML to 'product.xml'")
        with open("product.xml", "wb") as f:
            f.write(product_xml)

        logger.debug("Submitting new product to IriusRisk")
        response = requests.post(url, data=data, files={"fileName": open("product.xml", "r")}, headers=headers)
        logger.debug(f"Response received {response.status_code}: {response.text}")
        response.close()

    def create_product_xml(self, diagram_schema, draft="false"):
        xml_project = etree.Element("project", ref=self.id, name=self.name, revision="1", type="STANDARD", status="OPEN", enabled="true", modelUpdated="", priority="0", tags="", workflowState="", locked="false")
        etree.SubElement(xml_project, "desc")
        xml_diagram = etree.SubElement(xml_project, "diagram", draft=draft)
        xml_schema = etree.SubElement(xml_diagram, "schema")
        xml_schema.text = str(base64.b64encode(diagram_schema), "utf-8")
        xml_trustzones = etree.SubElement(xml_project, "trustZones")
        for trustzone in self.trustzones:
            etree.SubElement(xml_trustzones, "trustZone", ref=trustzone["id"], name=trustzone["name"])
        etree.SubElement(xml_project, "questions")
        etree.SubElement(xml_project, "assets")
        xml_settings = etree.SubElement(xml_project, "settings")
        xml_issue_trackers = etree.SubElement(xml_settings, "issueTrackers")
        xml_jira = etree.SubElement(xml_issue_trackers, "jira")
        etree.SubElement(xml_jira, "fields")
        xml_dataflows = etree.SubElement(xml_project, "dataflows")
        for dataflow in self.dataflows:
            xml_dataflow = etree.SubElement(xml_dataflows, "dataflow", name=dataflow["name"], ref=dataflow["id"], source=dataflow["from"], target=dataflow["to"])
            etree.SubElement(xml_dataflow, "assets")
            etree.SubElement(xml_dataflow, "tags")
        etree.SubElement(xml_project, "udts")
        xml_components = etree.SubElement(xml_project, "components")
        for component in self.components:
            xml_component = etree.SubElement(xml_components, "component", ref=component["id"], name=component["name"], desc="", library="", parentComponentRef="", componentDefinitionRef=component["component_definition"], asvsVersion="4")
            etree.SubElement(xml_component, "tags")
            etree.SubElement(xml_component, "questions")
            xml_component_trustzones = etree.SubElement(xml_component, "trustZones")
            etree.SubElement(xml_component_trustzones, "trustZone", ref=component["trustzone"])
            etree.SubElement(xml_component, "assets")
            xml_component_settings = etree.SubElement(xml_component, "settings")
            xml_component_issue_trackers = etree.SubElement(xml_component_settings, "issueTrackers")
            xml_component_jira = etree.SubElement(xml_component_issue_trackers, "jira") 
            etree.SubElement(xml_component_jira, "fields")
            etree.SubElement(xml_component, "weaknesses")
            etree.SubElement(xml_component, "controls")
            etree.SubElement(xml_component, "usecases")
        etree.SubElement(xml_project, "threadFixScans")

        return etree.tostring(xml_project, pretty_print=True, xml_declaration=True, encoding='utf-8', method='xml') 

    def recreate_diagram(self, diagram):
        if self.product_exists():
            self.delete_product()
        self.create_product(diagram)

    def upsert_diagram(self, diagram):
        if self.product_exists():
            self.update_product(diagram)
        else:
            self.create_product(diagram)

    def run_rules(self):
        url = self.irius_url(f"/rules/product/{self.id}")
        response = requests.put(url, headers=self.headers())
        logger.debug(f"Response received {response.status_code}: {response.text}")
        response.close()

    def load_schema(self):
        if not self.schema:
            schema_path = pkg_resources.resource_filename('startleft', os.path.join('data', 'otm_schema.json'))
            logger.debug(f"Loading schema from {schema_path}")
            with open(schema_path, "r") as f:
                schema = yaml.load(f, Loader=yaml.BaseLoader)
                self.schema = Schema(schema)

    def validate_otm(self):
        self.load_schema()
        logger.debug(f"--- Schema to validate against ---\n{self.schema.json()}\n--- End of schema ---")
        self.schema.validate(self.otm)
        return self.schema
