import warnings
from typing import Union

from deepdiff import DeepDiff

from otm.otm.entity.otm import Otm
from slp_base.slp_base.otm_file_loader import OtmFileLoader
from slp_base.slp_base.schema import Schema

public_cloud_id = 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
public_cloud_name = 'Public Cloud'

private_secured_id = '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'
private_secured_name = 'Private Secured'

internet_id = 'f0ba7722-39b6-4c81-8290-a30a248bb8d9'
internet_name = 'Internet'


def __load_otm(otm: Union[dict, str, Otm]):
    if isinstance(otm, dict):
        return otm

    if isinstance(otm, Otm):
        return otm.json()

    if isinstance(otm, str):
        return OtmFileLoader().load(otm)


def __compare_otm_files(expected: dict,
                        actual: dict,
                        excluded_regex) -> DeepDiff:
    return DeepDiff(expected, actual, ignore_order=True, exclude_regex_paths=excluded_regex)


def __validate_otm_schema(otm) -> Schema:
    schema: Schema = Schema('otm_schema.json')
    schema.validate(otm)
    return schema


def validate_and_diff(actual: Union[dict, str, Otm], expected: Union[dict, str, Otm], excluded_regex):
    warnings.warn("This method is deprecated, use 'validate_and_compare' instead", DeprecationWarning)
    """
    Utils for validating otm has a correct Schema
    and OTM contains expected data
    """
    actual_otm = __load_otm(actual)
    expected_otm = __load_otm(expected)

    schema = __validate_otm_schema(actual_otm)
    if not schema.valid:
        return {'schema_errors': schema.errors}
    diff = __compare_otm_files(expected_otm, actual_otm, excluded_regex)
    if diff:
        return diff
    return {}


def validate_and_diff_otm(actual: dict, expected_filename: str, excluded_regex):
    warnings.warn("This method is deprecated, use 'validate_and_compare_otm' instead", DeprecationWarning)
    expected = OtmFileLoader().load(expected_filename)
    return validate_and_diff(actual, expected, excluded_regex)


def validate_and_compare_otm(actual: dict, expected_filename: str, excluded_regex):
    expected = OtmFileLoader().load(expected_filename)
    return validate_and_compare(actual, expected, excluded_regex)


def validate_and_compare(actual: Union[dict, str, Otm], expected: Union[dict, str, Otm], excluded_regex):
    """
    Utils for validating otm has a correct Schema
    and OTM contains expected data that returns
    both sides to compare in case of diff
    """
    actual_otm = __load_otm(actual)
    expected_otm = __load_otm(expected)

    schema = __validate_otm_schema(actual_otm)
    if not schema.valid:
        return {'schema_errors': schema.errors}
    diff = __compare_otm_files(expected_otm, actual_otm, excluded_regex)
    if diff:
        return diff.t1, diff.t2
    return {}, {}


def check_otm_trustzone(otm, position, trustzone_id, name):
    assert otm.trustzones[position].id == trustzone_id
    assert otm.trustzones[position].name == name


def check_otm_component(otm, position, component_type, name, parent_id=None, tags=()):
    assert otm.components[position].type == component_type
    assert otm.components[position].name == name

    if parent_id:
        assert otm.components[position].parent == parent_id

    for c_tag in tags:
        assert c_tag in otm.components[position].tags


def check_otm_dataflow(otm, position, source_node, destination_node, bidirectional=None):
    assert otm.dataflows[position].source_node == source_node
    assert otm.dataflows[position].destination_node == destination_node
    if bidirectional is not None:
        assert otm.dataflows[position].bidirectional is bidirectional


def check_otm_representations_size(otm):
    assert "size" in otm.json()["representations"][0].keys()
    assert "width" in otm.json()["representations"][0]["size"].keys()
    assert "height" in otm.json()["representations"][0]["size"].keys()


def filter_modules_by_type(modules, module_type):
    return list(filter(lambda component: component.tags[0] == module_type, modules))
