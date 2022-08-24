import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

PROCESSORS = [
        {'name': 'slp_base', 'type': 'processor', 'forbidden_dependencies': ['startleft', 'slp_cft', 'slp_tf', 'slp_mtmt']},
        {'name': 'slp_cft',  'type': 'processor', 'forbidden_dependencies': ['startleft', 'slp_tf', 'slp_mtmt']},
        {'name': 'slp_tf',   'type': 'processor', 'forbidden_dependencies': ['startleft', 'slp_cft', 'slp_mtmt']},
        {'name': 'slp_mtmt', 'type': 'processor', 'forbidden_dependencies': ['startleft', 'slp_cft', 'slp_tf']}
]

_general_modules_forbidden_dependencies = ['startleft'] + [processor['name'] for processor in PROCESSORS]
GENERAL_MODULES = [
        {'name': 'sl_util', 'type': 'general', 'forbidden_dependencies': _general_modules_forbidden_dependencies},
        {'name': 'otm',     'type': 'general', 'forbidden_dependencies': _general_modules_forbidden_dependencies}
]

# TODO Once agnostic processor resolving was implemented, prevent startleft to directly import concrete processors
STARTLEFT_MODULE = [{'name': 'startleft', 'type': 'general', 'forbidden_dependencies': []}]

ALL_MODULES = PROCESSORS + GENERAL_MODULES + STARTLEFT_MODULE




