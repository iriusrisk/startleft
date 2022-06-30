from enum import Enum

from startleft import messages


class ErrorCode(Enum):
    IAC_TO_OTM_EXIT_UNEXPECTED = (1, "IacToOtmUnexpectedError")
    IAC_TO_OTM_EXIT_VALIDATION_FAILED = (2, "IacToOtmValidationError")
    OTM_TO_IR_EXIT_UNEXPECTED = (3, "OtmToIrUnexpectedError")
    OTM_TO_IR_EXIT_VALIDATION_FAILED = (4, "OtmToIrValidationError")
    MAPPING_FILE_EXIT_VALIDATION_FAILED = (5, "MalformedMappingFile")
    DIAGRAM_TO_OTM_EXIT_VALIDATION_FAILED = (6, "DiagramToOtmValidationError")

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


class UnknownDiagramType(CommonError):
    message = messages.CANNOT_RECOGNIZE_GIVEN_DIAGRAM_TYPE
    http_status_code = 400
    system_exit_status = ErrorCode.IAC_TO_OTM_EXIT_UNEXPECTED


class IacFileNotValidError(CommonError):
    message = messages.IAC_FILE_IS_NOT_VALID
    http_status_code = 400
    error_code = ErrorCode.IAC_TO_OTM_EXIT_VALIDATION_FAILED

    def __init__(self, message: str):
        self.message = f"{self.message}. {message}"


class DiagramFileNotValidError(CommonError):
    message = messages.DIAGRAM_FILE_IS_NOT_VALID
    http_status_code = 400
    error_code = ErrorCode.DIAGRAM_TO_OTM_EXIT_VALIDATION_FAILED

    def __init__(self, message: str):
        self.message = f"{self.message}. {message}"


class ParsingError(CommonError):
    message = messages.NOT_PARSEABLE_SOURCE_FILES
    http_status_code = 400

    def __init__(self, message: str, error_code: ErrorCode):
        self.message = f"{self.message}. {message}"
        self.error_code = error_code
