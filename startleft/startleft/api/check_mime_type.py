from functools import wraps
from typing import Union, List

from fastapi import UploadFile

from otm.otm.provider import Provider
from slp_base.slp_base.errors import SourceFileNotValidError


def check_mime_type(file_name: str, file_type_name: str):
    """
    Check the mime type of the input file.
    Get the current file and provider by the arguments values
    """

    def _check_mime_type(file: UploadFile, source_mime_type: Provider):
        content_type = file.content_type
        if not content_type or content_type not in source_mime_type.valid_mime:
            title = f'Invalid {source_mime_type.provider_name} file'
            details = f'Invalid content type for file {file.filename}'
            msg = f'{file.filename} with content-type {content_type} is not valid,' \
                  f' the valid types are {source_mime_type.valid_mime}'
            raise SourceFileNotValidError(title, details, msg)

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
