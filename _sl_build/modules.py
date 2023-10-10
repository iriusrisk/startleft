import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

STARTLEFT_MODULE = {'name': 'startleft', 'type': 'general', 'allowed_imports': ['slp_base', 'otm', 'sl_util']}
# TODO Startleft needs to depend on TF and CFT processors until a decision is token about the search function
# TODO Startleft needs to depend on VISIO processors until a decision is token about the summary function
STARTLEFT_MODULE['allowed_imports'].extend(['slp_cft', 'slp_tf', 'slp_visio'])

# TODO Dependency between otm and sl_util must be removed
OTM_MODULE = {'name': 'otm', 'type': 'general', 'allowed_imports': ['sl_util']}

SL_UTIL_MODULE = {'name': 'sl_util', 'type': 'general', 'allowed_imports': ['otm']}

_slp_allowed_imports = ['slp_base', 'sl_util', 'otm']
PROCESSORS = [
    {'name': 'slp_base', 'type': 'processor', 'allowed_imports': _slp_allowed_imports},
    {'name': 'slp_cft', 'type': 'processor', 'provider_type': 'CLOUDFORMATION', 'allowed_imports': _slp_allowed_imports},
    {'name': 'slp_tf', 'type': 'processor', 'provider_type': 'TERRAFORM', 'allowed_imports': _slp_allowed_imports},
    {'name': 'slp_tfplan', 'type': 'processor', 'provider_type': 'TFPLAN', 'allowed_imports': _slp_allowed_imports},
    {'name': 'slp_visio', 'type': 'processor', 'provider_type': 'VISIO', 'allowed_imports': _slp_allowed_imports},
    {'name': 'slp_visio', 'type': 'processor', 'provider_type': 'LUCID', 'allowed_imports': _slp_allowed_imports},
    {'name': 'slp_mtmt', 'type': 'processor', 'provider_type': 'MTMT', 'allowed_imports': _slp_allowed_imports}
]

"""
 All the StartLeft modules are defined here, along with their dependencies. Further information is available in:
 https://iriusrisk.github.io/startleft/development/Architecture
"""
ALL_MODULES = [STARTLEFT_MODULE] + [OTM_MODULE] + [SL_UTIL_MODULE] + PROCESSORS
