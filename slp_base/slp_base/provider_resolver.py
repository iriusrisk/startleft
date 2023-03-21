from enum import Enum

from slp_base import OTMProcessor, MappingValidator, LoadingSourceFileError, ProviderNotFoundError


def _find_provider_classes(processor_name):
    processor_module = __import__(processor_name)

    processor_classes = {}
    for attr in dir(processor_module):
        cls = getattr(processor_module, attr)
        if isinstance(cls, type) and issubclass(cls, OTMProcessor):
            processor_classes['processor'] = cls
        elif isinstance(cls, type) and issubclass(cls, MappingValidator):
            processor_classes['mapping_validator'] = cls

    return processor_classes


class ProviderResolver:

    def __init__(self, processor_implementations):
        self.provider_classes = {processor['provider_type']: _find_provider_classes(processor['name'])
                                 for processor in processor_implementations if 'provider_type' in processor}

    def get_processor(self, source_type, *args, **kwargs) -> OTMProcessor:
        source_type = self.__check_and_normalize_source_type(source_type)
        return self.provider_classes[source_type]['processor'](*args, **kwargs)

    def get_mapping_validator(self, source_type, *args) -> MappingValidator:
        source_type = self.__check_and_normalize_source_type(source_type)
        return self.provider_classes[source_type]['mapping_validator'](*args)

    def __check_and_normalize_source_type(self, source_type) -> str:
        str_source_type = source_type.value if isinstance(source_type, Enum) else str(source_type)

        if str_source_type not in self.provider_classes:
            raise ProviderNotFoundError(f'{source_type} is not a supported type for source data')

        return str_source_type


