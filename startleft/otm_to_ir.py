import logging

from startleft.apiclient.calls.check_project_exists import CheckProjectExists
from startleft.apiclient.calls.create_project import CreateProject
from startleft.apiclient.calls.delete_project import DeleteProject
from startleft.apiclient.calls.update_project import UpdateProject
from startleft.mapping.otm_file_loader import OtmFileLoader
from startleft.validators.otm_validator import OtmValidator

logger = logging.getLogger(__name__)


class OtmToIr:
    """
    This class in in charge of the methods to send OTM files to IR
    """
    EXIT_UNEXPECTED = 3
    EXIT_VALIDATION_FAILED = 4

    def __init__(self, server, api_token):
        self.server = server
        self.api_token = api_token
        self.check_project_exists = CheckProjectExists(self.server, self.api_token)
        self.update_project = UpdateProject(self.server, self.api_token)
        self.create_project = CreateProject(self.server, self.api_token)
        self.delete_project = DeleteProject(self.server, self.api_token)

    def run(self, recreate, otm_file: str):

        logger.info("Validating OTM file")
        otm = OtmFileLoader().load(otm_file)
        OtmValidator().validate(otm)

        project_id: str = otm["project"]["id"]

        if recreate:
            logger.debug("Recreating diagram in IriusRisk")
            if self.check_project_exists.do_call(project_id):
                self.delete_project.do_call(project_id)

            self.create_project.do_call(otm_file)
        else:
            logger.debug("Upserting diagram to IriusRisk")
            if self.check_project_exists.do_call(project_id):
                self.update_project.do_call(project_id, otm_file)
            else:
                self.create_project.do_call(otm_file)
