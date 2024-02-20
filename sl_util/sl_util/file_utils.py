import csv
import json
import os
import tempfile
from typing import List

from magic import Magic
from starlette.datastructures import UploadFile

SUPPORTED_ENCODINGS = ['utf-8', 'utf-16', 'utf-8-ignore']


def copy_to_disk(diag_file: tempfile.SpooledTemporaryFile, suffix: str):
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as ntf:
        ntf.write(diag_file.read())
        return ntf


def delete(filename: str):
    os.unlink(filename)


def get_as_str(filename: str) -> str:
    with open(filename, 'r') as file:
        return file.read()


def get_as_dict(filename: str):
    return json.loads(get_byte_data(filename))


def get_byte_data(filename: str) -> bytes:
    with open(filename, 'rb') as f:
        iac_data = f.read()
    return iac_data


def get_byte_data_from_upload_file(upload_file: UploadFile) -> bytes:
    return upload_file.file.read()


def read_byte_data(data: bytes) -> str:
    for encoding in SUPPORTED_ENCODINGS:
        try:
            return data.decode(encoding=encoding)
        except UnicodeError:
            pass

    raise UnicodeError(f'File content cannot be decoded, supported encodings: {SUPPORTED_ENCODINGS}')


def get_file_type_by_content(file_content: bytes) -> str:
    return Magic(mime=True).from_buffer(file_content)


def get_file_type_by_name(file_name: str) -> str:
    return Magic(mime=True).from_file(file_name)


def write_list_of_dictionaries_to_csv(data: List[dict], fieldnames: List[str], file_path: str) -> None:
    """
    Write a list of dictionaries to a CSV file.

    Args:
        data: List of dictionaries to be written to CSV.
        fieldnames: Names of the CSV columns
        file_path: Path to the output CSV file.
    """

    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def __get_files_with_extensions(folder_path: str, extensions: List[str]) -> List[str]:
    """
    Get a list of files with specified extensions from a folder.

    Args:
        folder_path: Path to the folder to search for files.
        extensions: List of file extensions to include.

    Returns:
        List of file paths matching the specified extensions in the given folder.
    """
    files = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and any(filename.endswith(ext) for ext in extensions):
            files.append(file_path)
    return files


def get_source_files(source_files: List[str], extensions: List[str]) -> List[str]:
    """
    Get a list of source files to process.

    If source_files is empty, it searches for files with the given extensions
    in the current working directory.

    Args:
        source_files: List of source file paths or an empty list.
        extensions: Types of files to retrieve

    Returns:
        List of source file paths to process.
    """
    files = []
    if not source_files:
        files = __get_files_with_extensions(os.getcwd(), extensions)
    else:
        for source_file in source_files:
            if os.path.isfile(source_file):
                files.append(source_file)
            elif os.path.isdir(source_file):
                files.extend(__get_files_with_extensions(source_file, extensions))
    return files


def load_csv_into_dict(file_name):
    data = []
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Read the header row
        for row in reader:
            record = {}
            for i, value in enumerate(row):
                record[headers[i]] = value
            data.append(record)

    return data
