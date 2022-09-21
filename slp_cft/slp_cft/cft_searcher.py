import json
import logging

from slp_cft.slp_cft.load.cft_loader import CloudformationLoader
from slp_cft.slp_cft.parse.mapping.cft_sourcemodel import CloudformationSourceModel

logger = logging.getLogger(__name__)


def load_cft_data(sources) -> dict:
    cft_loader = CloudformationLoader(sources)
    cft_loader.load()

    return cft_loader.get_cloudformation()


class CloudformationSearcher:

    def __init__(self, sources: [bytes]):
        self.cft_data = load_cft_data(sources)
        self.source_model = CloudformationSourceModel(self.cft_data)

    def search(self, query: str):
        """
        Runs a JMESPath search query against the provided source files and outputs the matching results
        """
        logger.info(f"Searching for '{query}' in source:")
        logger.info(json.dumps(self.source_model.data, indent=2))
        logger.info("--- Results ---")
        logger.info(json.dumps(self.source_model.query(query), indent=2))
