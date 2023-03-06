import re
from typing import Tuple

from otm.otm.entity.otm import OTM
from otm.otm.entity.parent_type import ParentType
from otm.otm.entity.trustzone import Trustzone
from slp_tf.slp_tf.tfplan.tfplan_component import TfplanComponent


def trustzone_to_otm(trustzone: {}) -> Trustzone:
    return Trustzone(
        trustzone_id=trustzone['id'],
        name=trustzone['name'],
        type=trustzone['type'] if 'type' in trustzone else trustzone['id'],
    )


def get_mappings_by_type(mappings: []) -> {}:
    return {m['tf_type']: (m['otm_type'], m.get('configuration', {})) for m in filter(lambda m: type(m['tf_type']) == str, mappings)}


def get_mappings_by_regex(mappings: []) -> {}:
    return {m['otm_type']: (m['tf_type']['$regex'], m.get('configuration', {}))
            for m in filter(lambda m: type(m['tf_type']) == dict, mappings)}


class TfplanMapper:

    def __init__(self, otm: OTM, tfplan: {}, mappings: {}):
        self.otm = otm
        self.resources = tfplan['resource']
        self.mappings = mappings

        self.default_trustzone: Trustzone = trustzone_to_otm(self.mappings['default_trustzone'])
        self.mappings_by_type: {} = get_mappings_by_type(self.mappings['components'])
        self.mappings_by_regex: {} = get_mappings_by_regex(self.mappings['components'])

    def map(self):
        self.otm.components = self.__tfplan_resources_to_otm_components()
        self.otm.trustzones = [self.default_trustzone]

    def __tfplan_resources_to_otm_components(self) -> []:
        components = []

        for resource in self.resources:
            component = self.__map_resource_by_type(resource)

            if not component:
                component = self.__map_resource_by_regex(resource)

            if component:
                components.append(component)

        return components

    def __map_resource_by_type(self, resource: {}) -> TfplanComponent:
        resource_type = resource['resource_type']
        if resource_type in self.mappings_by_type:
            mapper = self.mappings_by_type[resource_type]
            return self.__build_otm_component(resource, mapper[0], mapper[1])

    def __map_resource_by_regex(self, resource: {}) -> TfplanComponent:
        mapper = self.__get_otm_type_by_regex(resource)
        if mapper:
            return self.__build_otm_component(resource, mapper[0], mapper[1])

    def __get_otm_type_by_regex(self, resource: {}) -> Tuple[str, str]:
        for otm_type, regex in self.mappings_by_regex.items():
            if re.match(regex[0], resource['resource_type']):
                return otm_type, regex[1]

    def __build_otm_component(self, resource: {}, otm_type: str, configuration: {}) -> TfplanComponent:
        return TfplanComponent(
            component_id=resource['resource_id'],
            name=resource['resource_name'],
            component_type=otm_type,
            parent=self.default_trustzone.id,
            parent_type=ParentType.TRUST_ZONE,
            tags=[resource['resource_type']],
            tf_resource_id=resource['resource_id'],
            tf_type=resource['resource_type'],
            configuration=configuration
        )
