import logging

from startleft.api.api_config import ApiConfig
from startleft.apiclient.calls.check_project_exists import CheckProjectExists
from startleft.apiclient.calls.create_project import CreateProject
from startleft.apiclient.calls.delete_project import DeleteProject
from startleft.apiclient.calls.update_project import UpdateProject
from startleft.mapping.otm_file_loader import OtmFileLoader
from startleft.validators.otm_validator import OtmValidator

logger = logging.getLogger(__name__)


def get_project_id(otm_file: str) -> int:
    logger.info("Validating OTM file")

    otm = OtmFileLoader().load(otm_file)
    OtmValidator().validate(otm)

    return otm


class IriusriskProjectRepository:
    """
    This class is in charge of the methods to send OTM files to IR
    """
    EXIT_UNEXPECTED = 3
    EXIT_VALIDATION_FAILED = 4

    def __init__(self, api_token, api_url: str = None):
        self.api_url = api_url or ApiConfig.get_iriusrisk_server()
        self.api_token = api_token
        self.check_project_exists = CheckProjectExists(self.api_url, self.api_token)
        self.ir_project_updater = UpdateProject(self.api_url, self.api_token)
        self.ir_project_creator = CreateProject(self.api_url, self.api_token)
        self.ir_project_deleter = DeleteProject(self.api_url, self.api_token)

    def exists(self, project_id: str) -> bool:
        return self.check_project_exists.do_call(project_id)

    def create(self, otm_file: str):
        self.ir_project_creator.do_call(otm_file)

    def update(self, project_id: str, otm_file: str):
        self.ir_project_updater.do_call(project_id, otm_file)

    def delete(self, project_id: str):
        self.ir_project_deleter.do_call(project_id)
