import re

import jmespath


def add_type_and_name(obj, component_type, component_name):
    new_obj = obj.copy()

    new_obj['Type'] = component_type
    new_obj['_key'] = component_name
    # Included with the purpose of maximize compatibility between mappings
    new_obj["tf_type"] = component_type
    new_obj['tf_name'] = component_name

    return new_obj


class TerraformCustomFunctions(jmespath.functions.Functions):
    @jmespath.functions.signature({'types': ['string']}, {'types': ['number']})
    def _func_tail(self, string, count):
        return string[-count:]

    @jmespath.functions.signature({'types': ['string']}, {'types': ['string']}, {'types': ['string']})
    def _func_re_sub(self, pattern, replace, s):
        return re.sub(pattern, replace, s)

    @jmespath.functions.signature({'types': ['object']})
    # For future reference: [*].{ src: @, flt: *|[0].b }[?flt == 'some text 2'].src
    # If squash returns an array of key'd dicts, the above filter would need to be used
    def _func_squash(self, obj):
        temp = []
        for k, v in obj.items():
            if isinstance(v, dict):
                v["_key"] = k
            temp.append(v)
        return temp

    @jmespath.functions.signature({'types': ['array', 'null']})
    def _func_squash_terraform(self, component_types_arr):
        source_objects = []

        # Squash will include: tf_type, tf_name and tf_props
        # with the purpose of maximize compatibility between mappings
        if component_types_arr is not None:
            for component_type_obj in component_types_arr:
                component_type, component_name_obj = list(component_type_obj.items())[0]
                source_object = {}
                if isinstance(component_name_obj, dict):
                    source_object["Type"] = component_type
                    source_object["tf_type"] = component_type
                    for component_name, properties in component_name_obj.items():
                        source_object["_key"] = component_name
                        source_object["tf_name"] = component_name
                        source_object["Properties"] = properties
                        source_object["tf_props"] = component_name
                source_objects.append(source_object)

        return source_objects

    @jmespath.functions.signature({'types': ['array', 'null']}, {'types': ['string']})
    def _func_get_starts_with(self, obj_arr, component_type):
        source_objects = []

        if obj_arr is not None:
            for obj in obj_arr:
                for c_type in obj:
                    if c_type.startswith(component_type):
                        for c_name in obj[c_type]:
                            new_obj = add_type_and_name(obj[c_type], c_type, c_name)
                            source_objects.append(new_obj)

        return source_objects

    @jmespath.functions.signature({'types': ['array', 'null']}, {'types': ['string']})
    def _func_get(self, obj_arr, component_type):
        source_objects = []

        if obj_arr is not None:
            for obj in obj_arr:
                for c_type in obj:
                    if c_type == component_type:
                        for c_name in obj[c_type]:
                            new_obj = add_type_and_name(obj[c_type], c_type, c_name)
                            source_objects.append(new_obj)

        return source_objects

    @jmespath.functions.signature({'types': ['array', 'null']}, {'types': ['string']})
    def _func_get_module_terraform(self, modules, module_type):
        source_objects = []

        if modules is not None:
            for module in modules:
                for c_type in module:
                    module_source = module[c_type]['source']
                    if module_source == module_type:
                        new_obj = add_type_and_name(module[c_type], module_source, c_type)
                        new_obj['module'] = True
                        source_objects.append(new_obj)

        return source_objects

    @jmespath.functions.signature({'types': ['string']}, {'types': ['string']})
    def _func_split(self, string, separator):
        return string.split(separator)


jmespath_options = jmespath.Options(custom_functions=TerraformCustomFunctions())


def jmespath_search(search_path, source):
    try:
        return jmespath.search(search_path, source, options=jmespath_options)
    except:
        return None
