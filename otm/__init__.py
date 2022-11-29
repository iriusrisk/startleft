######################################################################
# This folder is not actually intended to be a regular package       #
# HOWEVER, we need to keep this __init.py__ file in order to         #
# make it visible by other modules.                                  #
# In future versions, this package should be moved to a lib so       #
# that it will be an independent module instead of a "false" package #
######################################################################

# DON'T REMOVE: Module importer overwritten to prevent bidirectional dependencies
from _sl_build.secure_importer import override_module_importer
override_module_importer()


