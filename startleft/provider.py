from enum import Enum


class Provider(Enum):

    def __new__(cls, value, provider_name: str, def_map_file: str, provider_type: str):
        obj = str.__new__(cls, [value])
        obj._value_ = value
        obj.provider_name = provider_name
        obj.def_map_file = def_map_file
        obj.provider_type = provider_type

        return obj
