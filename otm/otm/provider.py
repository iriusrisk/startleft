from enum import Enum
from typing import List

from otm.otm.entity.representation import RepresentationType


class Provider(Enum):

    def __new__(cls, value, provider_name: str, provider_type: RepresentationType, valid_mime: List[str] = []):
        obj = str.__new__(cls, [value])
        obj._value_ = value
        obj.provider_name = provider_name
        obj.provider_type = provider_type
        obj.valid_mime = valid_mime

        return obj
