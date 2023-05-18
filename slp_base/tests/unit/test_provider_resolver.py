import sys
from unittest import TestCase
from unittest.mock import patch, Mock

import pytest

from slp_base import OTMProcessor, ProviderParser, MappingLoader, MappingValidator, ProviderLoader, ProviderValidator, \
    ProviderNotFoundError
from slp_base.slp_base.provider_resolver import ProviderResolver

_slp_allowed_imports = ['slp_base', 'sl_util', 'otm']
MOCKED_PROCESSORS = [
    {'name': 'slp_base_MOCKED', 'type': 'processor', 'allowed_imports': _slp_allowed_imports},
    {'name': 'slp_cft_MOCKED', 'type': 'processor', 'provider_type': 'CLOUDFORMATION',
     'allowed_imports': _slp_allowed_imports},
    {'name': 'slp_tf_MOCKED', 'type': 'processor', 'provider_type': 'TERRAFORM',
     'allowed_imports': _slp_allowed_imports},
    {'name': 'slp_mtmt_MOCKED', 'type': 'processor', 'provider_type': 'MTMT',
     'allowed_imports': _slp_allowed_imports}
]


class MockedOTMProcessor(OTMProcessor):
    def get_provider_validator(self) -> ProviderValidator:
        pass

    def get_provider_loader(self) -> ProviderLoader:
        pass

    def get_mapping_validator(self) -> MappingValidator:
        pass

    def get_mapping_loader(self) -> MappingLoader:
        pass

    def get_provider_parser(self) -> ProviderParser:
        pass


class MockedMappingValidator(MappingValidator):

    def validate(self):
        pass


class TestProviderResolver(TestCase):

    def setUp(self):
        for mocked_processor in MOCKED_PROCESSORS:
            sys.modules[mocked_processor['name']] = Mock()

    def tearDown(self):
        for mocked_processor in MOCKED_PROCESSORS:
            sys.modules.pop(mocked_processor['name'])

    def test_get_processor_ok(self):
        # GIVEN a mocked list of processors
        mocked_processors = MOCKED_PROCESSORS

        # AND an existing provider type
        provider_type = 'CLOUDFORMATION'

        # WHEN get_processor is called in ProviderResolver
        with patch('slp_base.slp_base.provider_resolver.getattr', return_value=MockedOTMProcessor), \
                patch('slp_base.slp_base.provider_resolver.dir',
                      return_value=['MockedOTMProcessor', 'MockedMappingValidator', 'Anything']):
            processor = ProviderResolver(mocked_processors).get_processor(provider_type)

        # THEN a processor for that provider is returned
        assert type(processor) == MockedOTMProcessor

    def test_get_mapping_validator(self):
        # GIVEN a mocked list of processors
        mocked_processors = MOCKED_PROCESSORS

        # AND an existing provider type
        provider_type = 'CLOUDFORMATION'

        # WHEN get_mapping_validator is called in ProviderResolver
        with patch('slp_base.slp_base.provider_resolver.getattr', return_value=MockedMappingValidator), \
                patch('slp_base.slp_base.provider_resolver.dir', return_value=['MockedOTMProcessor', 'MockedMappingValidator', 'Anything']):
            validator = ProviderResolver(mocked_processors).get_mapping_validator(provider_type)

        # THEN a processor for that provider is returned
        assert type(validator) == MockedMappingValidator

    def test_get_processor_type_not_found(self):
        # GIVEN a mocked list of processors
        mocked_processors = MOCKED_PROCESSORS

        # AND a non-existing provider type
        provider_type = 'UNKNOWN TYPE'

        # WHEN get_processor is called in ProviderResolver
        with patch('slp_base.slp_base.provider_resolver._find_provider_classes'):

            # THEN a ProviderNotFoundError is raised
            with pytest.raises(ProviderNotFoundError) as error_info:
                processor = ProviderResolver(mocked_processors).get_processor(provider_type)

        # AND the error message is right
        assert error_info.value.title == f'{provider_type} is not a supported type for source data'

    def test_mapping_validator_type_not_found(self):
        # GIVEN a mocked list of processors
        mocked_processors = MOCKED_PROCESSORS

        # AND a non-existing provider type
        provider_type = 'UNKNOWN TYPE'

        # WHEN get_processor is called in ProviderResolver
        with patch('slp_base.slp_base.provider_resolver._find_provider_classes'):

            # THEN a ProviderNotFoundError is raised
            with pytest.raises(ProviderNotFoundError) as error_info:
                ProviderResolver(mocked_processors).get_processor(provider_type)

        # AND the error message is right
        assert error_info.value.title == f'{provider_type} is not a supported type for source data'

    def test_get_processor_without_processors(self):
        # GIVEN no processors
        mocked_processors = []

        # AND any provider type
        provider_type = 'ANY TYPE'

        # WHEN get_processor is called in ProviderResolver
        with patch('slp_base.slp_base.provider_resolver._find_provider_classes'):
            # THEN a ProviderNotFoundError is raised
            with pytest.raises(ProviderNotFoundError) as error_info:
                ProviderResolver(mocked_processors).get_processor(provider_type)

        # AND the error message is right
        assert error_info.value.title == f'{provider_type} is not a supported type for source data'
