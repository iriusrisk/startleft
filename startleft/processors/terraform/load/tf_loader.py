import logging
from io import StringIO

import hcl2

from startleft.api.errors import LoadingIacFileError
from startleft.processors.base.provider_loader import ProviderLoader

logger = logging.getLogger(__name__)


def hcl2_reader(data):
    return hcl2.load(StringIO(initial_value=hcl2_data_as_str(data), newline=None))


def hcl2_data_as_str(data) -> str:
    return data if isinstance(data, str) else data.decode()


class TerraformLoader(ProviderLoader):
    """
    Builder for a Terraform class from the xml data
    """

    def __init__(self, source):
        self.source = source
        self.hcl2_reader = hcl2_reader
        self.terraform = None

    def load(self):
        self.__load_hcl2_data()

    def get_terraform(self):
        return self.terraform

    def __load_hcl2_data(self):
        if not self.source:
            msg = "IaC file is empty"
            raise LoadingIacFileError("IaC file is not valid", msg, msg)

        try:
            logger.debug(f"Loading iac data and reading as string")

            self.terraform= self.hcl2_reader(self.source)

            logger.debug("Source data loaded successfully")
        except Exception as e:
            detail = e.__class__.__name__
            message = e.__str__()
            raise LoadingIacFileError("IaC file is not valid", detail, message)



