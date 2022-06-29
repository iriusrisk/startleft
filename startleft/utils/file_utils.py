import os
import tempfile


class FileUtils:

    @staticmethod
    def copy_to_disk(diag_file: tempfile.SpooledTemporaryFile, suffix: str):
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as ntf:
            ntf.write(diag_file.read())
            return ntf

    @classmethod
    def delete(cls, filename: str):
        os.unlink(filename)

    @staticmethod
    def get_data(filename):
        with open(filename, 'r') as f:
            iac_data = f.read()
        return iac_data

    @staticmethod
    def get_byte_data(filename):
        with open(filename, 'rb') as f:
            iac_data = f.read()
        return iac_data
