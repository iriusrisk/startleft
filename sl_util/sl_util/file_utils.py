import os
import tempfile


def copy_to_disk(diag_file: tempfile.SpooledTemporaryFile, suffix: str):
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as ntf:
        ntf.write(diag_file.read())
        return ntf


def delete(filename: str):
    os.unlink(filename)


def get_data(filename):
    with open(filename, 'r') as f:
        iac_data = f.read()
    return iac_data


def get_byte_data(filename):
    with open(filename, 'rb') as f:
        iac_data = f.read()
    return iac_data
