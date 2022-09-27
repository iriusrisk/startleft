import json
import logging

from slp_tf.slp_tf.load.tf_loader import TerraformLoader
from slp_tf.slp_tf.parse.mapping.tf_sourcemodel import TerraformSourceModel

logger = logging.getLogger(__name__)


def load_tf_data(sources) -> dict:
    tf_loader = TerraformLoader(sources)
    tf_loader.load()

    return tf_loader.get_terraform()


class TerraformSearcher:

    def __init__(self, sources: [bytes]):
        self.tf_data = load_tf_data(sources)
        self.source_model = TerraformSourceModel(self.tf_data)

    def search(self, query: str):
        """
        Runs a JMESPath search query against the provided source files and outputs the matching results
        """
        logger.info(f"Searching for '{query}' in source:")
        logger.info(json.dumps(self.source_model.data, indent=2))
        logger.info("--- Results ---")
        logger.info(json.dumps(self.source_model.query(query), indent=2))
