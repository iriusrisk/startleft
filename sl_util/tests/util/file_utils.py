import os
from tempfile import SpooledTemporaryFile

from starlette.datastructures import UploadFile


def file_exists(path: str) -> bool:
    return os.path.isfile(path)


def get_upload_file(source: str) -> UploadFile:
    tmp_file = SpooledTemporaryFile()
    with open(source, "rb") as file:
        tmp_file.write(file.read())
    tmp_file.seek(0)

    return UploadFile(filename=os.path.split(source)[1], file=tmp_file)


def generate_temporary_file(size_in_bytes: int, filename: str = "temp.txt") -> bytes:
    temporary_file = SpooledTemporaryFile()
    temporary_file.write(b'0' * size_in_bytes)
    temporary_file.seek(0)

    return UploadFile(filename=filename, file=temporary_file).file.read()
