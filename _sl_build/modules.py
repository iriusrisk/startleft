import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

PROCESSORS = [
    {'name': 'slp_base', 'type': 'processor',
     'forbidden_dependencies': ['startleft', 'slp_cft', 'slp_tf', 'slp_visio', 'slp_mtmt']},
    {'name': 'slp_cft', 'type': 'processor', 'provider_type': 'CLOUDFORMATION',
     'forbidden_dependencies': ['startleft', 'slp_tf', 'slp_visio', 'slp_mtmt']},
    {'name': 'slp_tf', 'type': 'processor', 'provider_type': 'TERRAFORM',
     'forbidden_dependencies': ['startleft', 'slp_cft', 'slp_visio', 'slp_mtmt']},
    {'name': 'slp_visio', 'type': 'processor', 'provider_type': 'VISIO',
     'forbidden_dependencies': ['startleft', 'slp_cft', 'slp_tf', 'slp_mtmt']},
    {'name': 'slp_visio', 'type': 'processor', 'provider_type': 'LUCID',
     'forbidden_dependencies': ['startleft', 'slp_cft', 'slp_tf', 'slp_mtmt']},
    {'name': 'slp_mtmt', 'type': 'processor', 'provider_type': 'MTMT',
     'forbidden_dependencies': ['startleft', 'slp_cft', 'slp_tf', 'slp_visio']}
]

_general_modules_forbidden_dependencies = ['startleft'] + [processor['name'] for processor in PROCESSORS]
GENERAL_MODULES = [
        {'name': 'sl_util', 'type': 'general', 'forbidden_dependencies': _general_modules_forbidden_dependencies},
        {'name': 'otm',     'type': 'general', 'forbidden_dependencies': _general_modules_forbidden_dependencies}
]

# TODO Startleft needs to depend on TF and CFT processors until a decision is token about the search function
_startleft_forbidden_dependencies = [p['name'] for p in PROCESSORS if 'provider_type' in p and p['name'] not in ['slp_cft', 'slp_tf']]
STARTLEFT_MODULE = [{'name': 'startleft', 'type': 'general', 'forbidden_dependencies': _startleft_forbidden_dependencies}]

ALL_MODULES = PROCESSORS + GENERAL_MODULES + STARTLEFT_MODULE




