import json
import logging
from typing import Optional

from typing.io import IO

from startleft.api.errors import OtmGenerationError
from startleft.iac.iac_to_otm import IacToOtm
from startleft.iac.iac_type import IacType
from startleft.mapping.mapping_file_loader import MappingFileLoader
from startleft.otm.otm import OTM
from startleft.otm.otm_file_loader import OtmFileLoader
from startleft.otm.otm_validator import OtmValidator
from startleft.validators.generic_mapping_validator import GenericMappingValidator
from startleft.validators.iac_validator import IacValidator

logger = logging.getLogger(__name__)

DEFAULT_OTM_FILENAME = 'threatmodel.otm'


class OtmProject:
    def __init__(self, project_id: str, project_name: str, otm_filename: str, otm: OTM):
        self.otm = otm
        self.otm_filename = otm_filename
        self.project_id = project_id
        self.project_name = project_name

    @staticmethod
    def from_otm_file(otm_filename: str, project_id: str = None, project_name: str = None):
        otm = OtmProject.load_and_validate_otm_file(otm_filename)

        project_id = project_id or otm['project']['id']
        project_name = project_name or otm['project']['name']

        return OtmProject(project_id, project_name, otm_filename, otm)

    @staticmethod
    def from_otm_stream(otm_stream: str, project_id: str = None, project_name: str = None):
        otm = OtmProject.validate_otm_stream(otm_stream)
        project_id = project_id or otm['project']['id']
        project_name = project_name or otm['project']['name']

        return OtmProject(project_id, project_name, None, otm)

    @staticmethod
    def from_iac_file_to_otm_stream(project_id: str, project_name: str, iac_type: IacType, iac_data: [bytes],
                                    mapping_data_list: [bytes]):
        IacValidator(iac_data, iac_type).validate()
        logger.info("Parsing IaC file to OTM")
        iac_to_otm = IacToOtm(project_name, project_id, iac_type)
        iac_to_otm.run(iac_type, mapping_data_list, iac_data)
        return OtmProject.from_otm_stream(iac_to_otm.get_otm_stream(), project_id, project_name)

    @staticmethod
    def validate_iac_mappings_file(mapping_files: [Optional[IO]]):
        logger.debug("Validating IaC mapping files")
        iac_mapping = MappingFileLoader().load(mapping_files)
        GenericMappingValidator('iac_mapping_schema.json').validate(iac_mapping)

    @staticmethod
    def validate_diagram_mappings_file(mapping_files: [Optional[IO]]):
        logger.debug("Validating Diagram mapping files")
        diagram_mapping = MappingFileLoader().load(mapping_files)
        GenericMappingValidator('diagram_mapping_schema.json').validate(diagram_mapping)

    @staticmethod
    def validate_otm_stream(otm_stream: str) -> {}:
        logger.debug("Validating OTM stream")
        OtmValidator().validate(otm_stream)
        return otm_stream

    @staticmethod
    def load_and_validate_otm_file(otm_filename: str) -> {}:
        logger.info("Loading and validating OTM file")
        otm = OtmFileLoader().load(otm_filename)
        OtmValidator().validate(otm)
        return otm

    def get_otm_as_json(self):
        logger.info("getting OTM contents as JSON")
        return json.dumps(self.otm, indent=2)

    def otm_to_file(self, out_file: str):
        logger.info(f"Writing OTM file to '{out_file}'")
        try:
            with open(out_file, "w") as f:
                json.dump(self.otm, f, indent=2)
        except Exception as e:
            logger.error(f"Unable to create the threat model: {e}")
            raise OtmGenerationError("Unable to create the OTM", e.__class__.__name__, str(e.__cause__))
