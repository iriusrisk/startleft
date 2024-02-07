import logging
import os

import xmlschema

from sl_util.sl_util.file_utils import get_file_type_by_content
from slp_base import ProviderValidator, DiagramFileNotValidError, DiagramType
from slp_base.slp_base.provider_validator import generate_size_error, generate_content_type_error, generate_schema_error

logger = logging.getLogger(__name__)
path = os.path.dirname(__file__)

class AbacusValidator(ProviderValidator):

    def __init__(self):
        super(AbacusValidator, self).__init__()


    # def validate(self):
    #     logger.info('Validating Abacus file')

