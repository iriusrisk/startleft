import logging
from io import StringIO

import hcl2
from deepmerge import always_merger

from slp_base import LoadingIacFileError
from slp_base import ProviderLoader

logger = logging.getLogger(__name__)


def hcl2_reader(data):
    return hcl2.load(StringIO(initial_value=hcl2_data_as_str(data), newline=None))


def hcl2_data_as_str(data) -> str:
    return data if isinstance(data, str) else data.decode()


def raise_empty_sources_error():
    msg = "IaC file is empty"
    raise LoadingIacFileError("IaC file is not valid", msg, msg)


class TerraformLoader(ProviderLoader):
    """
    Builder for a Terraform class from the xml data
    """

    def __init__(self, sources):
        self.sources = sources
        self.hcl2_reader = hcl2_reader
        self.terraform = None

    def load(self):
        self.__load_source_files()

    def get_terraform(self):
        return self.terraform

    def __load_source_files(self):
        if not self.sources:
            raise_empty_sources_error()

        for source in self.sources:
            self.__merge_hcl2_data(self.__load_hcl2_data(source))

        if not self.terraform:
            raise_empty_sources_error()

    def __merge_hcl2_data(self, tf_data):
        self.terraform = always_merger.merge(self.terraform, tf_data)

    def __load_hcl2_data(self, source):
        try:
            logger.debug(f"Loading iac data and reading as string")

            tf_data = self.hcl2_reader(source)

            logger.debug("Source data loaded successfully")

            return tf_data
        except Exception as e:
            detail = e.__class__.__name__
            message = e.__str__()
            raise LoadingIacFileError("IaC file is not valid", detail, message)
