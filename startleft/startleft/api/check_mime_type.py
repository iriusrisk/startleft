from functools import wraps
from typing import Union, List

from fastapi import UploadFile

from otm.otm.provider import Provider
from slp_base.slp_base.errors import SourceFileNotValidError
from slp_base.slp_base.provider_validator import generate_content_type_error


def check_mime_type(file_name: str, file_type_name: str, exception=SourceFileNotValidError):
    """
    Check the mime type of the input file.
    Get the current file and provider by the arguments values
    """

    def _check_mime_type(file: UploadFile, source_mime_type: Provider):
        content_type = file.content_type
        if not content_type or content_type not in source_mime_type.valid_mime:
            raise generate_content_type_error(source_mime_type, file_name, exception)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            source_file: Union[UploadFile, List[UploadFile]] = kwargs.get(file_name)
            source_type: Provider = kwargs.get(file_type_name)
            if source_file and source_type:
                source_file_list = source_file if isinstance(source_file, List) else [source_file]
                for file in source_file_list:
                    _check_mime_type(file, source_type)
            return func(*args, **kwargs)

        return wrapper

    return decorator
