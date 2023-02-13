from otm.otm.entity.component import OtmComponent


class TfplanComponent(OtmComponent):

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
            parent_type=parent_type,
            tags=tags
        )
        self.tf_resource_id: str = tf_resource_id
        self.tf_type: str = tf_type

