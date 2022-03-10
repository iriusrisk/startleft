import logging

from startleft.api.api_config import ApiConfig
from startleft.project.iriusrisk_project_repository import IriusriskProjectRepository
from startleft.project.otm_project import OtmProject

logger = logging.getLogger(__name__)


class OtmProjectService:
    def __init__(self, server_token: str, server_url: str = None):
        self.project_repository = IriusriskProjectRepository(
            server_url or ApiConfig.get_iriusrisk_server(), server_token)

    def create_project(self, otm_project: OtmProject):
        logger.debug(f"Creating new project with id {otm_project.project_id}")
        self.project_repository.create(otm_project.otm_filename)

    def update_project(self, otm_project: OtmProject):
        logger.debug(f"Updating project with id {otm_project.project_id}")
        self.project_repository.update(otm_project.project_id, otm_project.otm_filename)

    def recreate_project(self, otm_project: OtmProject):
        logger.debug("Recreating diagram in IriusRisk")
        if self.project_repository.exists(otm_project.project_id):
            logger.debug(f"Project {otm_project.project_id} exists, so it has to be deleted")
            self.project_repository.delete(otm_project.project_id)

        logger.debug(f"Creating new project with id {otm_project.project_id}")
        self.project_repository.create(otm_project.otm_filename)

    def update_or_create_project(self, otm_project: OtmProject):
        logger.debug("Upserting diagram to IriusRisk")
        if self.project_repository.exists(otm_project.project_id):
            logger.debug(f"Project {otm_project.project_id} exists, so it is updated")
            self.project_repository.update(otm_project.project_id, otm_project.otm_filename)
        else:
            logger.debug(f"Project {otm_project.project_id} does not exists, so it has to be created")
            self.project_repository.create(otm_project.otm_filename)
