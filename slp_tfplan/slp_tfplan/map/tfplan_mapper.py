import re
from functools import singledispatch
from typing import List

from otm.otm.entity.parent_type import ParentType
from otm.otm.entity.trustzone import Trustzone
from slp_tfplan.slp_tfplan.map.mapping import Mapping, TrustZoneMapping, ComponentMapping
from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanComponent, TFPlanOTM


@singledispatch
def _match_resource(label, resource: str):
    return resource == label


@_match_resource.register(list)
def _match_resource_by_list(label: List[str], resource: str):
    return resource in label


@_match_resource.register(dict)
def _match_resource_by_dict(label: dict, resource: str):
    return re.match(label.get('$regex'), resource)


def trustzone_to_otm(trustzone: TrustZoneMapping) -> Trustzone:
    return Trustzone(
        trustzone_id=trustzone.id,
        name=trustzone.name,
        type=trustzone.type,
        trustrating=trustzone.trust_rating
    )


class TFPlanMapper:

    def __init__(self, otm: TFPlanOTM, tfplan: {}, mapping: Mapping):
        self.otm = otm
        self.resources = tfplan['resource']
        self.mapping = mapping

        self.default_trustzone: Trustzone = trustzone_to_otm(self.mapping.default_trustzone)

    def map(self):
        self.otm.components = self.__tfplan_resources_to_otm_components()
        self.otm.trustzones = [self.default_trustzone]

    def __tfplan_resources_to_otm_components(self) -> []:
        components = []

        for resource in self.resources:
            if self.__exist_resource_as_skip(resource):
                continue

            component = \
                self.__map_resource_by_mapping_components(resource) or \
                self.__map_resource_by_catch_all(resource)

            if component:
                components.append(component)

        return components

    def __exist_resource_as_skip(self, resource: {}) -> bool:
        resource_type = resource['resource_type']
        return resource_type in self.mapping.label_to_skip

    def __map_resource_by_mapping_components(self, resource: dict) -> TFPlanComponent:
        for component in self.mapping.components:
            if _match_resource(component.label, resource['resource_type']):
                return self.__build_otm_component(resource, component)

    def __map_resource_by_catch_all(self, resource: dict) -> TFPlanComponent:
        if self.mapping.catch_all:
            if _match_resource(self.mapping.catch_all.label, resource['resource_type']):
                return self.__build_otm_component(resource, self.mapping.catch_all)

    def __build_otm_component(self, resource: {}, component: ComponentMapping) -> TFPlanComponent:
        return TFPlanComponent(
            component_id=resource['resource_id'],
            name=resource['resource_name'],
            component_type=component.type,
            parent=self.default_trustzone.id,
            parent_type=ParentType.TRUST_ZONE,
            tags=[resource['resource_type']],
            tf_resource_id=resource['resource_id'],
            tf_type=resource['resource_type'],
            configuration=component.configuration
        )
