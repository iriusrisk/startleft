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
