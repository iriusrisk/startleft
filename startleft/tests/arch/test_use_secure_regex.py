import ast
import os
import unittest
from unittest import TestCase


def get_files_with_imported_library(library_name, excluded_dirs=(), excluded_files=()) -> list[str]:
    if excluded_dirs is None:
        excluded_dirs = []
    this_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = f'{this_dir}/../../../'
    checked_files = []
    matches = []
    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        for file in files:
            if file.endswith('.py') and file not in excluded_files:
                checked_files.append(file)
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read(), filename=file_path)
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            for alias in node.names:
                                if alias.name == library_name:
                                    matches.append(file)
                                    continue
                        elif isinstance(node, ast.ImportFrom):
                            if node.module == library_name:
                                matches.append(file)
                                continue

    return matches


class TestUseSecureRegex(TestCase):

    def test_no_re_import(self):
        excluded_dirs = ['venv', '.eggs', 'build']
        excluded_files = ['diagram_mapper.py', 'visio.py', 'ip_utils.py', 'cli.py', 'version_scheme.py']
        matches = get_files_with_imported_library('re', excluded_dirs=excluded_dirs, excluded_files=excluded_files)

        self.assertEqual([], matches,
                         "There are files importing the insecure re library. Please use the secure_regex instead")

    def test_no_re2_import(self):
        excluded_dirs = ['venv', '.eggs', 'build']
        matches = get_files_with_imported_library('re2', excluded_dirs=excluded_dirs)

        self.assertEqual(['secure_regex.py'], matches,
                         "There are files importing the re2 library. Only the secure_regex should import it."
                         "Please use the secure_regex instead of importing re2 directly")
