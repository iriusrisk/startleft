from enum import Enum

from startleft.messages import messages


class ErrorCode(Enum):
    IAC_TO_OTM_EXIT_UNEXPECTED = (1, "IacToOtmUnexpectedError")
    IAC_TO_OTM_EXIT_VALIDATION_FAILED = (2, "IacToOtmValidationError")
    OTM_TO_IR_EXIT_UNEXPECTED = (3, "OtmToIrUnexpectedError")
    OTM_TO_IR_EXIT_VALIDATION_FAILED = (4, "OtmToIrValidationError")
    MAPPING_FILE_EXIT_VALIDATION_FAILED = (5, "MalformedMappingFile")

    def __init__(self, system_exit_status, error_type):
        self.system_exit_status = system_exit_status
        self.error_type = error_type

    def __str__(self):
        return f'{self.exit_value}'


class CommonError(Exception):
    message: str
    http_status_code: int
    error_code: ErrorCode


class OTMInconsistentIdsError(CommonError):
    message = messages.INCONSISTENT_IDS
    http_status_code = 500
    error_code = ErrorCode.OTM_TO_IR_EXIT_VALIDATION_FAILED


class OTMSchemaNotValidError(CommonError):
    message = messages.OTM_SCHEMA_IS_NOT_VALID
    http_status_code = 500
    error_code = ErrorCode.OTM_TO_IR_EXIT_VALIDATION_FAILED


class OTMFileNotFoundError(CommonError):
    message = messages.OTM_FILE_NOT_FOUND
    http_status_code = 500
    error_code = ErrorCode.OTM_TO_IR_EXIT_UNEXPECTED


class MappingFileNotFoundError(CommonError):
    message = messages.MAPPING_FILE_NOT_FOUND
    http_status_code = 500
    error_code = ErrorCode.IAC_TO_OTM_EXIT_UNEXPECTED


class MappingFileSchemaNotValidError(CommonError):
    message = messages.MAPPING_FILE_SCHEMA_NOT_VALID
    http_status_code = 400
    error_code = ErrorCode.MAPPING_FILE_EXIT_VALIDATION_FAILED

    def __init__(self, message: str):
        self.message = f"{self.message}. {message}"


class WriteThreatModelError(CommonError):
    message = messages.ERROR_WRITING_THREAT_MODEL
    http_status_code = 500
    error_code = ErrorCode.IAC_TO_OTM_EXIT_UNEXPECTED
