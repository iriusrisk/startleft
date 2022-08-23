import logging

import yaml

from startleft.api.errors import LoadingIacFileError
from startleft.processors.base.provider_loader import ProviderLoader

logger = logging.getLogger(__name__)


def yaml_reader(data):
    return yaml.load(yaml_data_as_str(data), Loader=yaml.BaseLoader)


def yaml_data_as_str(data) -> str:
    return data if isinstance(data, str) else data.decode()


class CloudformationLoader(ProviderLoader):
    """
    Builder for a Cloudformation class from the xml data
    """

    def __init__(self, source):
        self.source = source
        self.yaml_reader = yaml_reader
        self.cloudformation = None

    def load(self):
        self.__load_hcl2_data()

    def get_cloudformation(self):
        return self.cloudformation

    def __load_hcl2_data(self):
        if not self.source:
            msg = "IaC file is empty"
            raise LoadingIacFileError("IaC file is not valid", msg, msg)

        try:
            logger.debug(f"Loading iac data and reading as string")

            self.cloudformation= self.yaml_reader(self.source)

            logger.debug("Source data loaded successfully")
        except Exception as e:
            detail = e.__class__.__name__
            message = e.__str__()
            raise LoadingIacFileError("IaC file is not valid", detail, message)



