import logging
import os

import pkg_resources
import yaml
from deepmerge import always_merger

from startleft.mapper import TrustzoneMapper, ComponentMapper, DataflowMapper
from startleft.schema import Schema

logger = logging.getLogger(__name__)


class Transformer:
    def __init__(self, source_model=None, threat_model=None):
        self.source_model = source_model
        self.threat_model = threat_model
        self.map = {}
        self.id_map = {}
        self.schema = None

    def load_schema(self):
        schema_path = pkg_resources.resource_filename('startleft', os.path.join('data', 'mapping_schema.json'))
        logger.debug(f"Loading schema from {schema_path}")
        with open(schema_path, "r") as f:
            schema = yaml.load(f, Loader=yaml.BaseLoader)
            self.schema = Schema(schema)

    def validate_mapping(self):
        self.load_schema()
        logger.debug(f"--- Schema to validate against ---\n{self.schema.json()}\n--- End of schema ---")
        self.schema.validate(self.map)
        return self.schema

    def load(self, mapping):
        logger.debug('Loading mapping file')
        always_merger.merge(self.map, mapping)

    def build_lookup(self):
        if "lookup" in self.map:
            self.source_model.lookup = self.map["lookup"]

    def transform_trustzones(self):
        for mapping in self.map["trustzones"]:
            mapper = TrustzoneMapper(mapping)
            mapper.id_map = self.id_map
            for trustzone in mapper.run(self.source_model):
                # If no components are linked to a trustzone it shouldn't appear in the OTM
                for x in self.map["components"]:
                    if x.get("parent", "") == trustzone["type"]:
                        self.threat_model.add_trustzone(**trustzone)
                        break

    def transform_components(self):
        components = []
        catchall = []
        skip = []
        for mapping in self.map["components"]:
            mapper = ComponentMapper(mapping)
            mapper.id_map = self.id_map
            for component in mapper.run(self.source_model):
                if isinstance(mapping["$source"], dict):
                    if "$skip" in mapping["$source"]:
                        skip.append(component)
                        continue
                    elif "$catchall" in mapping["$source"]:
                        catchall.append(component)
                        continue
    
                components.append(component)
                
        results = []
        for component in components:
            skip_this = False
            for skip_component in skip:
                if component["id"] == skip_component["id"]:
                    logger.debug("Skipping component '{}'".format(component["id"]))
                    skip_this = True
                    break
            if not skip_this:
                results.append(component)

        for component in catchall:
            skip_this = False
            for skip_component in skip:
                if component["id"] == skip_component["id"]:
                    logger.debug("Skipping catchall component '{}'".format(component["id"]))
                    skip_this = True
                    break
            for current_component in results:
                if component["id"] == current_component["id"]:
                    logger.debug("Catchall component already added '{}'".format(component["id"]))
                    skip_this = True
                    break
            if not skip_this:
                results.append(component)

        for component in results:
            self.threat_model.add_component(**component)

    def transform_dataflows(self):
        for mapping in self.map["dataflows"]:
            mapper = DataflowMapper(mapping)
            mapper.id_map = self.id_map
            for dataflow in mapper.run(self.source_model):
                self.threat_model.add_dataflow(**dataflow)

    def run(self):
        self.build_lookup()
        self.transform_trustzones()
        self.transform_components()
        self.transform_dataflows()
