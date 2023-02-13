from enum import Enum


class ParentType(Enum):
    """
    Reference: https://github.com/iriusrisk/OpenThreatModel#parent-object
    """
    TRUST_ZONE = 'trustZone'
    COMPONENT = 'component'

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def __hash__(self) -> int:
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)

