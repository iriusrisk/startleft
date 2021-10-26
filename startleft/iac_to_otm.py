import json
import logging

import hcl2
import xmltodict
import yaml

from startleft import otm, sourcemodel, transformer
from startleft.api.errors import WriteThreatModelError
from startleft.mapping.mapping_file_loader import MappingFileLoader
from startleft.validators.mapping_validator import MappingValidator

logger = logging.getLogger(__name__)


class IacToOtm:
    """
    This class in in charge of the methods to convert IaC code to OTM files
    """
    EXIT_UNEXPECTED = 1
    EXIT_VALIDATION_FAILED = 2

    def __init__(self, name, id):
        self.otm = otm.OTM(name, id)
        self.source_model = sourcemodel.SourceModel()
        self.source_model.otm = self.otm
        self.transformer = transformer.Transformer(source_model=self.source_model, threat_model=self.otm)
        self.mapping_file_loader = MappingFileLoader()
        self.mapping_validator = MappingValidator()

        self.source_loader_map = {
            'JSON': self.load_yaml_source,
            'YAML': self.load_yaml_source,
            'CLOUDFORMATION': self.load_yaml_source,
            'HCL2': self.load_hcl2_source,
            'TERRAFORM': self.load_hcl2_source,
            'XML': self.load_xml_source
        }

    def load_xml_source(self, filename):
        logger.debug(f"Loading XML source file: {filename}")
        if isinstance(filename, str):
            with open(filename, 'rb') as f:
                self.source_model.load(xmltodict.parse(f.read(), xml_attribs=True))
        else:
            self.source_model.load(xmltodict.parse(filename.read(), xml_attribs=True))

    def load_yaml_source(self, filename):
        logger.debug(f"Loading YAML source file: {filename}")
        if isinstance(filename, str):
            with open(filename, 'r') as f:
                self.source_model.load(yaml.load(f, Loader=yaml.BaseLoader))
        else:
            self.source_model.load(yaml.load(filename, Loader=yaml.BaseLoader))

    def load_hcl2_source(self, filename):
        logger.debug(f"Loading HCL2 source file: {filename}")
        if isinstance(filename, str):
            with open(filename, 'r') as f:
                self.source_model.load(hcl2.load(f))
        else:
            self.source_model.load(hcl2.load(filename))

    def load_source_files(self, loader, filenames):
        logger.debug(f"Parsing IaC source files of type {type} to OTM")
        if isinstance(filenames, str):
            filenames = [filenames]        
        for filename in filenames:
            logger.debug(f"Parsing source file '{filename}'")
            try:
                loader(filename)
            except FileNotFoundError:
                logger.warning(f"Cannot find source file '{filename}', skipping")

    def write_otm(self, out_file):
        logger.info(f"Writing threat model to '{out_file}'")
        try:
            with open(out_file, "w") as f:
                json.dump(self.otm.json(), f, indent=2)
        except Exception as e:
            logger.error(f"Unable to create the threat model: {e}")
            raise WriteThreatModelError()

    def run(self, type, map_filenames, out_file, filenames):
        """
        Parses selected source files and maps them to the Open Threat Model format
        """
        loader = self.source_loader_map[type.upper()]
        self.load_source_files(loader, filenames)

        iac_mapping = self.mapping_file_loader.load(map_filenames)
        self.mapping_validator.validate(iac_mapping)

        self.transformer.run(iac_mapping)
        self.write_otm(out_file)

    def search(self, type, query, filenames):
        """
        Runs a JMESPath search query against the provided source files and outputs the matching results
        """        
        loader = self.source_loader_map[type.upper()]
        self.load_source_files(loader, filenames)
        
        logger.info(f"Searching for '{query}' in source:")
        logger.info(json.dumps(self.source_model.data, indent=2))
        logger.info("--- Results ---")
        logger.info(json.dumps(self.source_model.query(query), indent=2))
