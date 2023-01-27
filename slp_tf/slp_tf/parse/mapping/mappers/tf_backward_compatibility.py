import re
from collections.abc import MutableMapping


def is_type_and_name_string(key):
    return re.match(rf"^aws_[\w-]+\.[\w-]+$", key)


def return_name_from_type_and_name_string(key):
    if is_type_and_name_string(key):
        return re.match(rf"^aws_[\w-]+\.([\w-]+)$", key).group(1)


class TfIdMapDictionary(MutableMapping):
    """
    Add backward compatibility to previous mapping files that links are by resource_name
    """

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

    def __getitem__(self, key):
        return self.backward_compatibility(key)

    def __setitem__(self, key, value):
        self.store[key] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __contains__(self, key):
        try:
            return bool(self.backward_compatibility(key))
        except KeyError:
            return False

    def backward_compatibility(self, key):
        try:
            return self.store[key]
        except KeyError:
            # match type.name == name
            for iter_key, iter_value in self.store.items():
                if re.match(rf"^aws_[\w-]+\.{key}$", iter_key):
                    return iter_value
            # match name == type.name
            if is_type_and_name_string(key):
                name = return_name_from_type_and_name_string(key)
                return self.store[name]
        raise KeyError(key)


class TfDataflowNodeId(str):
    """
    Add backward compatibility to previous dataflows linked by _key
    """

    def __init__(self, string):
        self.value = string

    def __eq__(self, other):
        if isinstance(other, TfDataflowNodeId):
            result = self.value == other.value
            if not result:
                # match type.name == name
                if is_type_and_name_string(self.value) and not is_type_and_name_string(other.value):
                    return return_name_from_type_and_name_string(self.value) == other.value
                # match name == type.name
                elif not is_type_and_name_string(self.value) and is_type_and_name_string(other.value):
                    return self.value == return_name_from_type_and_name_string(other.value)
            return result
        else:
            return self.value == other

    def __hash__(self):
        return str.__hash__(self.value)
