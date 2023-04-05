import builtins
import importlib

from _sl_build.modules import ALL_MODULES


def _build_dependencies_map():
    module_dependencies = [{module['name']: module['allowed_imports']} for module in ALL_MODULES]
    return {name: dependencies for module in module_dependencies for name, dependencies in module.items()}


_module_names = [module['name'] for module in ALL_MODULES]
_allowed_imports = _build_dependencies_map()


def _get_base_module_name(full_name):
    return full_name.split('.')[0] if type(full_name) == str else None


def _is_module_restricted(importing_module: str, imported_module: str):
    base_importing_module = _get_base_module_name(importing_module)
    base_imported_module = _get_base_module_name(imported_module)

    if not base_importing_module or not base_imported_module or \
            base_importing_module == base_imported_module or \
            base_importing_module not in _module_names or base_imported_module not in _module_names:
        return False

    return base_imported_module not in _allowed_imports[base_importing_module]


def _secure_importer(name, globals=None, locals=None, fromlist=(), level=0):
    importing_module = globals['__name__'] if globals else None

    if _is_module_restricted(importing_module, name):
        raise ImportError(f'Importing {name} from {importing_module} is forbidden')

    return importlib.__import__(name, globals, locals, fromlist, level)


def override_module_importer():
    builtins.__import__ = _secure_importer
