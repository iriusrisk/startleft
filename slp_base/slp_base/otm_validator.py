import logging

from slp_base.slp_base.errors import OtmResultError
from slp_base.slp_base.schema import Schema

logger = logging.getLogger(__name__)


class OtmValidator:

    def __init__(self):
        self.schema: Schema = Schema('otm_schema.json')

    def validate(self, otm):
        self.__validate_otm_schema(otm)
        self.__check_otm_files(otm)
        logger.info('OTM file validated successfully')

    def __validate_otm_schema(self, otm: {}):
        logger.debug('Validating OTM file schema')
        self.schema.validate(otm)
        if self.schema.valid:
            logger.info('OTM file schema is valid')
        if not self.schema.valid:
            logger.error('OTM file schema is not valid')
            logger.error(f'--- Schema errors---\n{self.schema.errors}\n--- End of schema errors ---')
            raise OtmResultError('OTM file does not comply with the schema', 'Schema error',
                                 str(self.schema.errors))

    def __check_otm_files(self, otm):
        logger.debug('Checking IDs consistency on OTM file')
        if self.__check_otm_ids(otm):
            logger.info('OTM file has consistent IDs')
        else:
            msg = 'OTM file has inconsistent IDs'
            logger.error(msg)
            raise OtmResultError('Schema error', 'Parsing provided files result in an invalid OTM file', msg)

    def __check_otm_ids(self, otm):
        all_valid_ids = set()
        repeated_ids = set()
        parent_ids = set()
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
            parent_ids.add(trustzone_id)

        for parent_id in parent_ids:
            if parent_id not in all_valid_ids:
                wrong_component_parent_ids.add(parent_id)

        for dataflow in otm['dataflows']:
            if dataflow['id'] in all_valid_ids:
                repeated_ids.add(dataflow['id'])
            elif dataflow['id'] not in all_valid_ids:
                all_valid_ids.add(dataflow['id'])

            if dataflow['source'] not in all_valid_ids:
                wrong_dataflow_from_ids.add(dataflow['source'])

            if dataflow['destination'] not in all_valid_ids:
                wrong_dataflow_to_ids.add(dataflow['destination'])

        if wrong_component_parent_ids:
            logger.error(f"Component parent identifiers inconsistent: {wrong_component_parent_ids}")

        if wrong_dataflow_from_ids:
            logger.error(f"Dataflow 'source' identifiers inconsistent: {wrong_dataflow_from_ids}")

        if wrong_dataflow_to_ids:
            logger.error(f"Dataflow 'destination' identifiers inconsistent: {wrong_dataflow_to_ids}")

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
