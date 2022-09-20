from enum import Enum


class Provider(Enum):

    def __new__(cls, value, provider_name: str, provider_type: str):
        obj = str.__new__(cls, [value])
        obj._value_ = value
        obj.provider_name = provider_name
        obj.provider_type = provider_type

        return obj