from enum import Enum


class ErrorCode(Enum):

    IAC_LOADING_ERROR = (1, 400)
    IAC_NOT_VALID = (2, 400)
    IAC_UNEXPECTED = (5, 500)

    DIAGRAM_LOADING_ERROR = (11, 400)
    DIAGRAM_NOT_VALID = (12, 400)
    DIAGRAM_UNEXPECTED = (15, 500)

    MAPPING_LOADING_ERROR = (21, 400)
    MAPPING_FILE_NOT_VALID = (22, 400)
    MAPPING_UNEXPECTED = (25, 500)

    OTM_BUILDING_ERROR = (41, 400)
    OTM_RESULT_ERROR = (42, 400)
    OTM_UNEXPECTED = (45, 500)

    def __init__(self, system_exit_status, http_status):
        self.http_status = http_status
        self.system_exit_status = system_exit_status

    def __str__(self):
        return f'{self.exit_value}'


class CommonError(Exception):
    http_status_code: int
    error_code: ErrorCode

    def __init__(self, title, detail, message):
        self.title = title
        self.detail = detail
        self.message = message

    def __str__(self):
        self.__class__.__name__


class IacFileNotValidError(CommonError):
    error_code = ErrorCode.IAC_NOT_VALID


class DiagramFileNotValidError(CommonError):
    error_code = ErrorCode.DIAGRAM_NOT_VALID


class MappingFileNotValidError(CommonError):
    error_code = ErrorCode.MAPPING_FILE_NOT_VALID


class LoadingIacFileError(CommonError):
    error_code = ErrorCode.IAC_LOADING_ERROR


class LoadingDiagramFileError(CommonError):
    error_code = ErrorCode.DIAGRAM_LOADING_ERROR


class OtmBuildingError(CommonError):
    error_code = ErrorCode.OTM_BUILDING_ERROR
