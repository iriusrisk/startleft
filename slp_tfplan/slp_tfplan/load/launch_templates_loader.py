from slp_tfplan.slp_tfplan.objects.tfplan_objects import TfplanOTM, TfplanLaunchTemplate
from slp_tfplan.slp_tfplan.load.resource_data_extractors import security_groups_ids_from_network_interfaces

LAUNCH_TEMPLATE_TYPES = ['aws_launch_template']


def build_launch_template(resource: {}) -> TfplanLaunchTemplate:
    return TfplanLaunchTemplate(
        launch_template_id=resource['resource_id'],
        security_groups_ids=security_groups_ids_from_network_interfaces(resource)
    )


class TfplanLaunchTemplateLoader:

    def __init__(self, otm: TfplanOTM, tfplan: {}):
        self.otm = otm
        self.resources = tfplan['resource']

    def load(self):
        for resource in self.resources:
            if resource['resource_type'] in LAUNCH_TEMPLATE_TYPES:
                self.otm.launch_templates.append(build_launch_template(resource))
