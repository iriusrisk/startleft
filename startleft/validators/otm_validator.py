import logging
import sys

from startleft.validators.schema import Schema, OtmSchema

logger = logging.getLogger(__name__)


class OtmValidator:
    EXIT_UNEXPECTED = 3
    EXIT_VALIDATION_FAILED = 4

    def __init__(self):
        self.schema: Schema = OtmSchema()

    def validate(self, otm):
        self.__validate_otm_schema(otm)
        self.__check_otm_files(otm)

    def __validate_otm_schema(self, otm: {}):
        logger.debug("Validating OTM schema")
        self.schema.validate(otm)
        if self.schema.valid:
            logger.info('OTM file is valid')
        if not self.schema.valid:
            logger.error('OTM file is not valid')
            logger.error(f"--- Schema errors---\n{self.schema.errors}\n--- End of schema errors ---")
            sys.exit(OtmValidator.EXIT_VALIDATION_FAILED)

    def __check_otm_files(self, otm):
        logger.debug("Checking IDs consistency on OTM file")
        if self.__check_otm_ids(otm):
            logger.info('OTM file has consistent IDs')
        else:
            logger.error('OTM file has inconsistent IDs')
            sys.exit(OtmValidator.EXIT_VALIDATION_FAILED)

    def __check_otm_ids(self, otm):
        all_valid_ids = set()
        repeated_ids = set()
        wrong_component_parent_ids = set()
        wrong_dataflow_from_ids = set()
        wrong_dataflow_to_ids = set()

        for trustzone in otm['trustZones']:
            if trustzone['id'] in all_valid_ids:
                repeated_ids.add(trustzone['id'])
            elif trustzone['id'] not in all_valid_ids:
                all_valid_ids.add(trustzone['id'])

        for component in otm['components']:
            if component['id'] in all_valid_ids:
                repeated_ids.add(component['id'])
            elif component['id'] not in all_valid_ids:
                all_valid_ids.add(component['id'])

            trustzone_id = self.__get_trustzone_id(component)
            if trustzone_id not in all_valid_ids:
                wrong_component_parent_ids.add(trustzone_id)

        for dataflow in otm['dataflows']:
            if dataflow['id'] in all_valid_ids:
                repeated_ids.add(dataflow['id'])
            elif dataflow['id'] not in all_valid_ids:
                all_valid_ids.add(dataflow['id'])

            if dataflow['from'] not in all_valid_ids:
                wrong_dataflow_from_ids.add(dataflow['from'])

            if dataflow['to'] not in all_valid_ids:
                wrong_dataflow_to_ids.add(dataflow['to'])

        if wrong_component_parent_ids:
            logger.error(f"Component parent identifiers inconsistent: {wrong_component_parent_ids}")

        if wrong_dataflow_from_ids:
            logger.error(f"Dataflow 'from' identifiers inconsistent: {wrong_dataflow_from_ids}")

        if wrong_dataflow_to_ids:
            logger.error(f"Dataflow 'to' identifiers inconsistent: {wrong_dataflow_to_ids}")

        if repeated_ids:
            logger.error(f"Repeated identifiers inconsistent: {repeated_ids}")

        return (not wrong_component_parent_ids and
                not wrong_dataflow_from_ids and
                not wrong_dataflow_to_ids and
                not repeated_ids)

    def __get_trustzone_id(self, trustzone: dict):
        if 'trustZone' in trustzone['parent']:
            return trustzone['parent']['trustZone']
        else:
            return trustzone['parent']['component']
