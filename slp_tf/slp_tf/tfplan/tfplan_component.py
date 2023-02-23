from otm.otm.entity.parent_type import ParentType
from otm.otm.entity.component import Component


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
            parent_type=ParentType.COMPONENT if parent == 'component' else ParentType.TRUST_ZONE,
            tags=tags
        )
        self.tf_resource_id: str = tf_resource_id
        self.tf_type: str = tf_type

