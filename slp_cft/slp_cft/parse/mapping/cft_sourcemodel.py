import json

import jmespath
from deepmerge import always_merger

from sl_util.sl_util.secure_regex import SecureRegexWrapper as re


class CloudformationCustomFunctions(jmespath.functions.Functions):
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

    @jmespath.functions.signature({'types': ['array', 'null']}, {'types': ['string']})
    def _func_get_starts_with(self, obj_arr, component_type):
        source_objects = []

        if obj_arr is not None:
            for obj in obj_arr:
                for c_type in obj:
                    if c_type.startswith(component_type):
                        for c_name in obj[c_type]:
                            new_obj = self.add_type_and_name(obj[c_type], c_type, c_name)
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
                            new_obj = self.add_type_and_name(obj[c_type], c_type, c_name)
                            source_objects.append(new_obj)

        return source_objects

    @jmespath.functions.signature({'types': ['string']}, {'types': ['string']})
    def _func_split(self, string, separator):
        return string.split(separator)

    def add_type_and_name(self, obj, component_type, component_name):
        new_obj = obj.copy()

        new_obj['Type'] = component_type
        new_obj['_key'] = component_name

        return new_obj


class CloudformationSourceModel:
    def __init__(self, data=None, otm=None):
        self.data = data or {}
        self.otm = otm
        self.lookup = {}
        self.jmespath_options = jmespath.Options(custom_functions=CloudformationCustomFunctions())

    def load(self, data):
        always_merger.merge(self.data, data)

    def json(self):
        return json.dumps(self.data, indent=2)

    def query(self, query):
        return jmespath.search(query, self.data, options=self.jmespath_options)

    def search(self, obj, source=None):
        if isinstance(obj, str):
            return obj

        if isinstance(obj, list):
            results = []
            for element in obj:
                mapping_path_value = self.search(element, source)
                if isinstance(mapping_path_value, list):
                    results = results + mapping_path_value
                else:
                    results = results + [str(mapping_path_value)]
            return results

        if isinstance(obj, dict):
            if "$lookup" in obj:
                keys = self.search(obj["$lookup"], source)

                if isinstance(keys, str):
                    return self.lookup[keys]
                elif isinstance(keys, list):
                    results = []
                    for key in keys:
                        results.append(self.lookup[key])
                    return results

            if "$skip" in obj:
                return self.search(obj["$skip"], source)

            if "$parent" in obj:
                return self.search(obj["$parent"], source)

            if "$singleton" in obj:
                return self.search(obj["$singleton"], source)

            if "$root" in obj:
                return jmespath.search(obj["$root"], self.data, options=self.jmespath_options)

            if "$path" in obj:
                if "$searchParams" in obj["$path"]:
                    return self.__search_with_default(obj, source, "$path")
                else:
                    return self.__jmespath_search(obj["$path"], source)

            if "$format" in obj:
                return obj["$format"].format(**source)

            if "$catchall" in obj:
                return self.search(obj["$catchall"], source)

            if "$children" in obj:
                return self.search(obj["$children"], source)

            if "$search" in obj:
                results = []
                search_type = obj["$search"]["$type"]
                ref_value = jmespath.search(obj["$search"]["$ref"], source, options=self.jmespath_options)
                for refobj in self.otm.objects_by_type(search_type):
                    search_values = jmespath.search(obj["$search"]["$path"], refobj.source,
                                                    options=self.jmespath_options)
                    if isinstance(search_values, list):
                        if ref_value in search_values:
                            results.append(refobj.id)
                    else:
                        if ref_value == search_values:
                            results.append(refobj.id)
                return results

            if "$findFirst" in obj:
                if "$searchParams" in obj["$findFirst"]:
                    return self.__search_with_default(obj, source, "$findFirst")
                else:
                    return self.__find_first_search(obj["$findFirst"], source)

            if "$numberOfSources" in obj:
                return self.__multiple_source_search(source, obj)

            if "$hub" in obj:
                return self.search(obj["$hub"], source)

            if "$ip" in obj:
                return self.search(obj["$ip"], source)

            return obj

    def __search_with_default(self, obj, source, action):
        try:
            search_params = obj[action]["$searchParams"]

            if "searchPath" in search_params:
                if action == "$path":
                    search_result = self.__jmespath_search(search_params["searchPath"], source)
                elif action == "$findFirst":
                    search_result = self.__find_first_search(search_params["searchPath"], source)
                else:
                    return []

                if search_result is None:
                    if "defaultValue" in search_params:
                        try:
                            return search_params["defaultValue"]
                        except:
                            return []
                    else:
                        return []
                else:
                    return search_result
            else:
                return []
        except:
            return []

    def __jmespath_search(self, search_path, source):
        try:
            source_objects = jmespath.search(search_path, source, options=self.jmespath_options)
            if 'Ref' in source_objects:
                ref = source_objects['Ref']
                return jmespath.search("Parameters." + ref + ".Default || '" + ref + "'", self.data,
                                       options=self.jmespath_options)
            else:
                return source_objects
        except:
            return None

    def __find_first_search(self, search_path_root, source):
        for search_path in search_path_root:
            search_result = self.__jmespath_search(search_path, source)
            if search_result is not None:
                return search_result

    def __multiple_source_search(self, source, object):

        single_value = None
        multiple_value = None
        if "multipleSource" in object["$numberOfSources"]:
            multiple_value = self.search(object["$numberOfSources"]["multipleSource"], source)
        if "oneSource" in object["$numberOfSources"]:
            single_value = self.search(object["$numberOfSources"]["oneSource"], source)
        return single_value, multiple_value
