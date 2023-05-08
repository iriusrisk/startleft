import logging

from otm.otm.entity.parent_type import ParentType
from slp_base.slp_base.errors import OTMResultError
from slp_base.slp_base.schema import Schema

logger = logging.getLogger(__name__)


class OTMValidator:
    schema_filename = 'otm_schema.json'

    def __init__(self):
        self.schema: Schema = Schema.from_package('otm', self.schema_filename)

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
            raise OTMResultError('OTM file does not comply with the schema', 'Schema error',
                                 str(self.schema.errors))

    def __check_otm_files(self, otm):
        logger.debug('Checking IDs consistency on OTM file')
        if self.__check_otm_ids(otm):
            logger.info('OTM file has consistent IDs')
        else:
            msg = 'OTM file has inconsistent IDs'
            logger.error(msg)
            raise OTMResultError('Schema error', 'Parsing provided files result in an invalid OTM file', msg)

    def __check_otm_ids(self, otm):
        all_valid_ids = set()
        repeated_ids = set()
        parent_ids = set()
        wrong_component_parent_ids = set()
        wrong_dataflow_from_ids = set()
        wrong_dataflow_to_ids = set()

        if 'trustZones' in otm:
            for trustzone in otm['trustZones']:
                if trustzone['id'] in all_valid_ids:
                    repeated_ids.add(trustzone['id'])
                elif trustzone['id'] not in all_valid_ids:
                    all_valid_ids.add(trustzone['id'])

        if 'components' in otm:
            for component in otm['components']:
                if component['id'] in all_valid_ids:
                    repeated_ids.add(component['id'])
                elif component['id'] not in all_valid_ids:
                    all_valid_ids.add(component['id'])

                component_parent_id = self.__get_parent_id(component)
                parent_ids.add(component_parent_id)

            for parent_id in parent_ids:
                if parent_id not in all_valid_ids:
                    wrong_component_parent_ids.add(parent_id)

        if 'dataflows' in otm:
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


    @staticmethod
    def __get_parent_id(trustzone: dict):
        parent = ParentType.TRUST_ZONE if ParentType.TRUST_ZONE in trustzone['parent'] else ParentType.COMPONENT
        return trustzone['parent'][str(parent)]
