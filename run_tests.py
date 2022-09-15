import os

import pytest
from _pytest.config import ExitCode

from _sl_build.modules import ALL_MODULES

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

modules = ALL_MODULES


class StartleftTestsFailed(Exception):
    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


def get_module_tests_dirs() -> []:
    dirs = []

    for module in modules:
        dirs.append(ROOT_DIR + '/' + module['name'])

    return dirs


def get_main_tests_dirs() -> []:
    return [ROOT_DIR + '/tests/integration']


def run_pytest(test_dirs: []):
    args = [f'--junitxml={ROOT_DIR}/test-reports/report.xml']
    return pytest.main(args + test_dirs)

def run_all_tests():
    test_dirs = get_module_tests_dirs() + get_main_tests_dirs()
    test_result = run_pytest(test_dirs)

    if ExitCode.OK != test_result:
        raise StartleftTestsFailed


if __name__ == '__main__':
    run_all_tests()
