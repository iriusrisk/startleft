from otm.otm.entity.component import Component
from otm.otm.entity.parent_type import ParentType


class TfplanComponent(Component):

    def __init__(self,
                 component_id: str,
                 name: str,
                 component_type: str,
                 parent: str,
                 parent_type: ParentType,
                 tags: [str],
                 tf_resource_id: str = None,
                 tf_type: str = None,
                 configuration: {} = None):
        super().__init__(
            component_id=component_id,
            name=name, component_type=component_type,
            parent=parent, parent_type=parent_type,
            tags=tags
        )
        self.tf_resource_id: str = tf_resource_id
        self.tf_type: str = tf_type
        self.configuration = configuration or {}

    @property
    def is_singleton(self) -> bool:
        return self.configuration.get('singleton', False)

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, TfplanComponent):
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
