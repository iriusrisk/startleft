from deepdiff import DeepDiff

from startleft.otm.otm_file_loader import OtmFileLoader
from startleft.validators.schema import Schema

public_cloud_id = 'b61d6911-338d-46a8-9f39-8dcd24abfe91'
public_cloud_name = 'Public Cloud'

private_secured_id = '2ab4effa-40b7-4cd2-ba81-8247d29a6f2d'
private_secured_name = 'Private Secured'

internet_id = 'f0ba7722-39b6-4c81-8290-a30a248bb8d9'
internet_name = 'Internet'


def __compare_otm_files(expected_filename: str,
                        actual_filename: str,
                        excluded_regex) -> DeepDiff:
    expected = OtmFileLoader().load(expected_filename)
    actual = OtmFileLoader().load(actual_filename)
    return DeepDiff(expected, actual, ignore_order=True, exclude_regex_paths=excluded_regex)


def __validate_otm_schema(otm_filename) -> Schema:
    otm = OtmFileLoader().load(otm_filename)
    schema: Schema = Schema('otm_schema.json')
    schema.validate(otm)
    return schema


def validate_and_diff(actual_filename: str, expected_filename: str, excluded_regex):
    """
    Utils for validating otm has a correct Schema
    and OTM contains expected data
    """
    schema = __validate_otm_schema(actual_filename)
    if not schema.valid:
        return {'schema_errors': schema.errors}
    diff = __compare_otm_files(expected_filename, actual_filename, excluded_regex)
    if diff:
        return diff
    return {}


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


def check_otm_dataflow(otm, position, source_node, destination_node):
    assert otm.dataflows[position].source_node == source_node
    assert otm.dataflows[position].destination_node == destination_node


def check_otm_representations_size(otm):
    assert "size" in otm.json()["representations"][0].keys()
    assert "width" in otm.json()["representations"][0]["size"].keys()
    assert "height" in otm.json()["representations"][0]["size"].keys()
