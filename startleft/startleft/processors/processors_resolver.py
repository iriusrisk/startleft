from slp_base import IacType, LoadingSourceFileError, EtmType
from slp_cft import CloudformationProcessor, CloudformationMappingFileValidator
from slp_mtmt import MTMTProcessor
from slp_tf import TerraformProcessor, TerraformMappingFileValidator


# TODO Implement this resolver in an agnostic way, so it does not need to specificly import the specific processor implementations

def get_processor(source_type, id, name, source_data, mapping_data_list):
    if source_type == IacType.TERRAFORM:
        return TerraformProcessor(id, name, source_data, mapping_data_list)
    if source_type == IacType.CLOUDFORMATION:
        return CloudformationProcessor(id, name, source_data, mapping_data_list)
    if source_type == EtmType.MTMT:
        return MTMTProcessor(id, name, source_data, mapping_data_list)
    else:
        raise LoadingSourceFileError(f'{source_type} is not a supported type for source data')


def get_mapping_validator(source_type, mapping_data_list):
    if source_type == IacType.TERRAFORM:
        return TerraformMappingFileValidator(mapping_data_list)
    if source_type == IacType.CLOUDFORMATION:
        return CloudformationMappingFileValidator(mapping_data_list)
    else:
        raise LoadingSourceFileError(f'{source_type} is not a supported type for source data')
