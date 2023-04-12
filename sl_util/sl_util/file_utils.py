import os
import tempfile
from magic import Magic


def copy_to_disk(diag_file: tempfile.SpooledTemporaryFile, suffix: str):
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as ntf:
        ntf.write(diag_file.read())
        return ntf


def delete(filename: str):
    os.unlink(filename)


def get_data(filename: str) -> str:
    with open(filename, 'r') as f:
        iac_data = f.read()
    return iac_data


def get_byte_data(filename: str) -> bytes:
    with open(filename, 'rb') as f:
        iac_data = f.read()
    return iac_data


def read_byte_data(data: bytes, encoding: str = 'utf-8') -> str:
    return data.decode(encoding)


def get_file_type_by_content(file_content: bytes) -> str:
    return Magic(mime=True).from_buffer(file_content)


def get_file_type_by_name(file_name: str) -> str:
    return Magic(mime=True).from_file(file_name)
