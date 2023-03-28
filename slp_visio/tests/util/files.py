import os
import tempfile

from starlette.datastructures import UploadFile


def file_exists(path: str) -> bool:
    return os.path.isfile(path)


def get_temp_dir_files_count() -> int:
    tmp_dir_path = tempfile.gettempdir()
    return len([name for name in os.listdir(tmp_dir_path) if os.path.isfile(os.path.join(tmp_dir_path, name))])


def get_upload_file(source: str) -> UploadFile:
    tmp_file = tempfile.SpooledTemporaryFile()
    with open(source, "rb") as file:
        tmp_file.write(file.read())
    tmp_file.seek(0)

    return UploadFile(filename=os.path.split(source)[1], file=tmp_file)
