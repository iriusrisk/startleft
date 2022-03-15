import logging

from startleft.apiclient.base_api_client import BaseApiClient

logger = logging.getLogger(__name__)


class CreateProject(BaseApiClient):

    def do_call(self, otm_file):
        logger.debug("Creating project in IriusRisk")

        self.post(f"/products/otm", self._build_token_header(), otm_file)
