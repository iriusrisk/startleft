from typing import List

from slp_base import MappingFileNotValidError


class ComponentMapping:

    def __init__(self, component: {}):
        self.__component = component

    @property
    def label(self) -> str:
        return self.__component['label']

    @property
    def type(self) -> str:
        return self.__component['type']

    @property
    def configuration(self) -> dict:
        return {
            '$singleton': self.__component.get('$singleton', False)
        }

    def __str__(self) -> str:
        return f'{{label: {self.label}, type: {self.type}, configuration: {self.configuration}}}'


class TrustZoneMapping:

    def __init__(self, trustzone: {}):
        self.__trustzone = trustzone

    @property
    def id(self) -> str:
        return self.__trustzone['id']

    @property
    def type(self) -> str:
        return self.__trustzone['type']

    @property
    def name(self) -> str:
        return self.__trustzone['name']

    @property
    def trust_rating(self) -> int:
        trust_rating = self.__trustzone.get('risk', {}).get('trust_rating', None)
        return int(trust_rating) if trust_rating else None

    @property
    def is_default(self) -> bool:
        return self.__trustzone.get('$default', False)

    def __str__(self) -> str:
        return f'{{id: {self.id}, type: {self.type}, name: {self.name}, ' \
               f'trust_rating: {self.trust_rating}, is_default: {self.is_default}}}'


def _exist_trustzone(trustzone_id: str, trustzones: List[TrustZoneMapping]) -> bool:
    """
    Returns True if exists a TrustZone with the given identifier, returns False otherwise
    :param trustzone_id: The TrustZone identifier
    :param trustzones: The TrustZone list
    :return: Whether a TrustZone exists
    """
    return len(list(filter(lambda tz: tz.id == trustzone_id, trustzones))) > 0


class AttackSurface:

    def __init__(self, attack_surface: {}, trustzones: List[TrustZoneMapping]):
        self.__attack_surface = attack_surface
        self.__trustzones = trustzones
        self.__validate()

    def __validate(self):
        if not self.client:
            msg = 'Attack Surface must contain a client'
            raise MappingFileNotValidError('Mapping file not valid', msg, msg)

        if not self.__trustzone_id or not self.__trustzones \
                or not _exist_trustzone(self.__trustzone_id, self.__trustzones):
            msg = 'Attack Surface must contain a valid TrustZone'
            raise MappingFileNotValidError('Mapping file not valid', msg, msg)

    @property
    def client(self) -> str:
        return self.__attack_surface.get('client', None)

    @property
    def trustzone(self) -> TrustZoneMapping:
        return next(filter(lambda tz: tz.id == self.__trustzone_id, self.__trustzones))

    @property
    def __trustzone_id(self) -> str:
        return self.__attack_surface.get('trustzone', None)

    def __str__(self) -> str:
        return f'{{client: {self.client}, trustzone: {self.trustzone}}}'


def _exist_default_trustzone(trustzones: List[TrustZoneMapping]):
    return len(list(filter(lambda tz: tz.is_default, trustzones))) > 0


class Mapping:

    def __init__(self, mapping_dict: {}):
        self.__map = mapping_dict
        self.__validate()

    def __validate(self):
        if not self.trustzones:
            msg = 'Mapping file must contain at least one TrustZone'
            raise MappingFileNotValidError('Mapping file not valid', msg, msg)

        if not self.components:
            msg = 'Mapping file must contain at least one Component'
            raise MappingFileNotValidError('Mapping file not valid', msg, msg)

        if not _exist_default_trustzone(self.trustzones):
            msg = 'Mapping file must contain a default TrustZone'
            raise MappingFileNotValidError('Mapping file not valid', msg, msg)

    @property
    def default_trustzone(self) -> TrustZoneMapping:
        return next(filter(lambda tz: tz.is_default, self.trustzones))

    @property
    def trustzones(self) -> List[TrustZoneMapping]:
        return list(map(lambda e: TrustZoneMapping(e), self.__map.get('trustzones', [])))

    @property
    def components(self) -> List[ComponentMapping]:
        return list(map(lambda e: ComponentMapping(e), self.__map.get('components', [])))

    @property
    def label_to_skip(self) -> List[str]:
        return self.__map.get('configuration', {}).get('skip', [])

    @property
    def attack_surface(self) -> AttackSurface:
        attack_surface = self.__map.get('configuration', {}).get('attack_surface', None)
        if attack_surface:
            return AttackSurface(attack_surface, self.trustzones)

    @property
    def catch_all(self) -> ComponentMapping:
        catch_all_type = self.__map.get('configuration', {}).get('catch_all', None)
        if catch_all_type:
            return ComponentMapping({
                'label': {'$regex': r'^aws_\w*$'},
                'type': catch_all_type
            })

    def __str__(self) -> str:
        return f'{{default_trustzone: {self.default_trustzone}, trustzones: {self.trustzones}' \
               f'components: {self.components}, label_to_skip: {self.label_to_skip}' \
               f'attack_surface: {self.attack_surface}, catch_all: {self.catch_all}' \
               f'}}'
