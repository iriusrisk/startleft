from typing import List

from otm.otm.entity.component import Component
from otm.otm.entity.dataflow import Dataflow
from otm.otm.entity.otm import OTM
from otm.otm.entity.parent_type import ParentType
from otm.otm.entity.trustzone import Trustzone
from sl_util.sl_util.lang_utils import auto_repr
from slp_base import IacType


@auto_repr
class TFPlanComponent(Component):

    def __init__(self,
                 component_id: str,
                 name: str,
                 component_type: str,
                 parent: str,
                 parent_type: ParentType,
                 tags: [str],
                 clones_ids: [str] = None,
                 tf_resource_id: str = None,
                 tf_type: str = None,
                 configuration: {} = None):
        super().__init__(
            component_id=component_id,
            name=name, component_type=component_type,
            parent=parent, parent_type=parent_type,
            tags=tags
        )
        self.clones_ids = clones_ids
        self.tf_resource_id: str = tf_resource_id
        self.tf_type: str = tf_type
        self.configuration = configuration or {}

    @property
    def is_singleton(self) -> bool:
        return self.configuration.get('singleton', False)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, TFPlanComponent):
            return self.id == other.id \
                and self.name == other.name \
                and self.type == other.type \
                and self.parent == other.parent \
                and self.parent_type == other.parent_type \
                and self.source == other.source \
                and self.attributes == other.attributes \
                and self.threats == other.threats \
                and self.representations == other.representations \
                and self.tf_resource_id == other.tf_resource_id \
                and self.tf_type == other.tf_type \
                and self.configuration == other.configuration
        return False


@auto_repr
class TFPlanSecurityGroup:
    def __init__(self, security_group_id: str, ingress_sgs: List[str] = None, egress_sgs: List[str] = None):
        self.id = security_group_id
        self.ingress_sgs = ingress_sgs
        self.egress_sgs = egress_sgs


@auto_repr
class TFPlanLaunchTemplate:
    def __init__(self, launch_template_id: str, security_groups_ids: List[str]):
        self.id = launch_template_id
        self.security_groups_ids = security_groups_ids


@auto_repr
class TfplanOTM(OTM):

    def __init__(self,
                 project_id: str,
                 project_name: str,
                 components: List[TFPlanComponent],
                 security_groups: List[TFPlanSecurityGroup],
                 launch_templates: List[TFPlanLaunchTemplate],
                 dataflows: List[Dataflow],
                 default_trustzone: Trustzone = None):
        super().__init__(project_name, project_id, IacType.TERRAFORM)
        self.default_trustzone = default_trustzone
        self.trustzones = [self.default_trustzone]
        self.components = components or []
        self.security_groups = security_groups or []
        self.launch_templates = launch_templates or []
        self.dataflows = dataflows or []

    @property
    def mapped_resources_ids(self):
        return [component.id for component in self.components] + \
            [sg.id for sg in self.security_groups] + \
            [lt.id for lt in self.launch_templates]
