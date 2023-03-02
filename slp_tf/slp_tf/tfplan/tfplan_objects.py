from typing import List

from sl_util.sl_util.lang_utils import auto_repr
from otm.otm.entity.trustzone import Trustzone
from otm.otm.entity.otm import OTM
from otm.otm.entity.dataflow import Dataflow
from otm.otm.entity.parent_type import ParentType
from otm.otm.entity.component import Component
from slp_base import IacType


@auto_repr
class TfplanComponent(Component):
    def __init__(self,
                 component_id: str,
                 name: str,
                 component_type: str,
                 parent: str,
                 parent_type: str,
                 tags: [str],
                 tf_resource_id: str,
                 tf_type: str):
        super().__init__(
            component_id=component_id,
            name=name, component_type=component_type,
            parent=parent,
            parent_type=ParentType.COMPONENT if parent_type == 'component' else ParentType.TRUST_ZONE,
            tags=tags
        )
        self.tf_resource_id: str = tf_resource_id
        self.tf_type: str = tf_type


@auto_repr
class TfplanSecurityGroup:
    def __init__(self, security_group_id: str, ingress_sgs: List = None, egress_sgs: List = None):
        self.id = security_group_id
        self.ingress_sgs = ingress_sgs
        self.egress_sgs = egress_sgs


@auto_repr
class TfplanLaunchTemplate:
    def __init__(self, launch_template_id: str, security_groups_ids: List[str]):
        self.id = launch_template_id
        self.security_groups_ids = security_groups_ids


@auto_repr
class TfplanOTM(OTM):

    def __init__(self,
                 project_id: str,
                 project_name: str,
                 components: List[TfplanComponent],
                 security_groups: List[TfplanSecurityGroup],
                 launch_templates: List[TfplanLaunchTemplate],
                 dataflows: List[Dataflow],
                 default_trustzone: Trustzone = None):
        super().__init__(project_name, project_id, IacType.TERRAFORM)
        self.default_trustzone = default_trustzone
        self.trustzones = [self.default_trustzone]
        self.components = components
        self.security_groups = security_groups
        self.launch_templates = launch_templates
        self.dataflows = dataflows
