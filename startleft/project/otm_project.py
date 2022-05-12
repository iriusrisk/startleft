import json
import logging
from typing import Optional

from typing.io import IO

from startleft.diagram.visio_to_otm import VisioToOtm
from startleft.provider import Provider
from startleft.iac_to_otm import IacToOtm
from startleft.mapping.mapping_file_loader import MappingFileLoader
from startleft.mapping.otm_file_loader import OtmFileLoader
from startleft.otm import OTM
from startleft.utils.file_utils import FileUtils
from startleft.validators.mapping_validator import MappingValidator
from startleft.validators.otm_validator import OtmValidator

logger = logging.getLogger(__name__)

DEFAULT_OTM_FILENAME = 'threatmodel.otm'
VSDX_EXT = '.vsdx'


def get_default_iac_mapping_files(provider: Provider) -> [str]:
    return Provider(provider).def_map_file


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
    def from_iac_file(project_id: str, project_name: str, iac_type: Provider, iac_file: [Optional[IO]],
                      custom_iac_mapping_files: [Optional[IO]] = None, otm_filename: str = DEFAULT_OTM_FILENAME):
        mapping_iac_files = custom_iac_mapping_files or get_default_iac_mapping_files(iac_type)
        logger.info("Parsing IaC file to OTM")
        iac_to_otm = IacToOtm(project_name, project_id, iac_type)
        iac_to_otm.run(iac_type, mapping_iac_files, otm_filename, iac_file)

        return OtmProject.from_otm_file(otm_filename, project_id, project_name)

    @staticmethod
    def from_iac_file_to_otm_stream(project_id: str, project_name: str, iac_type: Provider, iac_file: [Optional[IO]],
                                    custom_iac_mapping_files: [Optional[IO]] = None):
        mapping_iac_files = custom_iac_mapping_files or get_default_iac_mapping_files(iac_type)
        logger.info("Parsing IaC file to OTM")
        iac_to_otm = IacToOtm(project_name, project_id, iac_type)
        iac_to_otm.run(iac_type, mapping_iac_files, None, iac_file)

        return OtmProject.from_otm_stream(iac_to_otm.get_otm_stream(), project_id, project_name)

    @staticmethod
    def from_diag_file_to_otm_stream(project_id: str, project_name: str, diag_type: Provider, diag_file: [Optional[IO]],
                                     custom_mapping_files: [Optional[IO]] = None):
        mapping_iac_files = custom_mapping_files or diag_type.def_map_file
        iac_mapping = MappingFileLoader().load(mapping_iac_files)
        MappingValidator('diagram_mapping_schema.json').validate(iac_mapping)

        logger.info("Parsing Diagram file to OTM")
        temp_diag_file = FileUtils.copy_to_disk(diag_file[0], VSDX_EXT)
        diag_to_otm = VisioToOtm(temp_diag_file.name)
        otm = diag_to_otm.run(iac_mapping, project_name, project_id)
        FileUtils.delete(temp_diag_file.name)
        return OtmProject.from_otm_stream(otm.json(), project_id, project_name)

    @staticmethod
    def validate_iac_mappings_file(mapping_files: [Optional[IO]]):
        logger.info("Validating IaC mapping files")
        iac_mapping = MappingFileLoader().load(mapping_files)
        MappingValidator('iac_mapping_schema.json').validate(iac_mapping)

    @staticmethod
    def validate_otm_stream(otm_stream: str) -> {}:
        logger.info("Validating OTM stream")
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
