from startleft.messages import messages

IAC_TO_OTM_EXIT_UNEXPECTED = 1
IAC_TO_OTM_EXIT_VALIDATION_FAILED = 2
OTM_TO_IR_EXIT_UNEXPECTED = 3
OTM_TO_IR_EXIT_VALIDATION_FAILED = 4


class CommonError(Exception):
    message: str
    http_status_code: int
    system_exit_status: int


class IriusUnauthorizedError(CommonError):
    message = messages.UNAUTHORIZED_EXCEPTION
    http_status_code = 401
    system_exit_status = OTM_TO_IR_EXIT_UNEXPECTED


class IriusTokenNotSettedError(CommonError):
    message = messages.UNAUTHORIZED_EXCEPTION
    http_status_code = 401
    system_exit_status = OTM_TO_IR_EXIT_UNEXPECTED


class IriusForbiddenError(CommonError):
    message = messages.FORBIDDEN_OPERATION
    http_status_code = 403
    system_exit_status = OTM_TO_IR_EXIT_UNEXPECTED


class IriusServerNotSettedError(CommonError):
    message = messages.IRIUS_SERVER_NOT_SETTED
    http_status_code = 500
    system_exit_status = OTM_TO_IR_EXIT_UNEXPECTED


class IriusCommonApiError(CommonError):
    message = messages.UNEXPECTED_API_ERROR
    http_status_code = 500
    system_exit_status = OTM_TO_IR_EXIT_UNEXPECTED

    def __init__(self, http_status_code: int, message: str):
        self.http_status_code = http_status_code
        self.message = message


class OTMInconsistentIdsError(CommonError):
    message = messages.INCONSISTENT_IDS
    http_status_code = 500
    system_exit_status = OTM_TO_IR_EXIT_VALIDATION_FAILED


class OTMSchemaNotValidError(CommonError):
    message = messages.OTM_SCHEMA_IS_NOT_VALID
    http_status_code = 500
    system_exit_status = OTM_TO_IR_EXIT_VALIDATION_FAILED


class OTMFileNotFoundError(CommonError):
    message = messages.OTM_FILE_NOT_FOUND
    http_status_code = 500
    system_exit_status = OTM_TO_IR_EXIT_UNEXPECTED


class MappingFileNotFoundError(CommonError):
    message = messages.MAPPING_FILE_NOT_FOUND
    http_status_code = 500
    system_exit_status = IAC_TO_OTM_EXIT_UNEXPECTED


class MappingFileSchemaNotValidError(CommonError):
    message = messages.MAPPING_FILE_SCHEMA_NOT_VALID
    http_status_code = 400
    system_exit_status = IAC_TO_OTM_EXIT_VALIDATION_FAILED

    def __init__(self, message: str):
        self.message = f"{self.message}. {message}"


class WriteThreatModelError(CommonError):
    message = messages.ERROR_WRITING_THREAT_MODEL
    http_status_code = 500
    system_exit_status = IAC_TO_OTM_EXIT_UNEXPECTED
