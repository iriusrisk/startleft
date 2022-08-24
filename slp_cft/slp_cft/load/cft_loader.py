import logging

import yaml
from deepmerge import always_merger

from slp_base.slp_base.errors import LoadingIacFileError
from slp_base.slp_base.provider_loader import ProviderLoader

logger = logging.getLogger(__name__)


def yaml_reader(data):
    return yaml.load(yaml_data_as_str(data), Loader=yaml.BaseLoader)


def yaml_data_as_str(data) -> str:
    return data if isinstance(data, str) else data.decode()


def raise_empty_sources_error():
    msg = "IaC file is empty"
    raise LoadingIacFileError("IaC file is not valid", msg, msg)


class CloudformationLoader(ProviderLoader):
    """
    Builder for a Cloudformation class from the xml data
    """

    def __init__(self, sources):
        self.sources = sources
        self.yaml_reader = yaml_reader
        self.cloudformation = None

    def load(self):
        self.__load_source_files()

    def get_cloudformation(self):
        return self.cloudformation

    def __load_source_files(self):
        if not self.sources:
            raise_empty_sources_error()

        for source in self.sources:
            self.__merge_cft_data(self.__load_cft_data(source))

        if not self.cloudformation:
            raise_empty_sources_error()

    def __merge_cft_data(self, cft_data):
        self.cloudformation = always_merger.merge(self.cloudformation, cft_data)

    def __load_cft_data(self, source) -> dict:
        try:
            logger.debug(f"Loading iac data and reading as string")

            cft_data = self.yaml_reader(source)

            logger.debug("Source data loaded successfully")

            return cft_data
        except Exception as e:
            detail = e.__class__.__name__
            message = e.__str__()
            raise LoadingIacFileError("IaC file is not valid", detail, message)
