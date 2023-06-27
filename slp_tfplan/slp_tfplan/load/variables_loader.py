from typing import Union

from slp_tfplan.slp_tfplan.objects.tfplan_objects import TFPlanOTM

LAUNCH_TEMPLATE_TYPES = ['aws_launch_template']


def _extract_value(value: {}) -> Union[list, str]:
    return isinstance(value, dict) and value.get('value', None)


class VariablesLoader:

    def __init__(self, otm: TFPlanOTM, tfplan: {}):
        self.otm = otm
        self.variables = tfplan.get('variables', {})

    def load(self):
        for k, v in self.variables.items():
            value = _extract_value(v)
            if value:
                self.otm.variables[k] = value
