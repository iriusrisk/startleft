from deepdiff import DeepDiff


def compare_dict(expected: dict, actual: dict, exclude_paths=None, exclude_regex=None) -> (dict, dict):
    diff = DeepDiff(expected, actual, ignore_order=True, exclude_paths=exclude_paths, exclude_regex_paths=exclude_regex)
    if diff:
        return diff.t1, diff.t2
    return {}, {}
