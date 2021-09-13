import jmespath
import json
import re
from deepmerge import always_merger


class CustomFunctions(jmespath.functions.Functions):
    @jmespath.functions.signature({'types': ['string']}, {'types': ['number']})
    def _func_tail(self, string, count):
        return string[count:]

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


class SourceModel:
    def __init__(self):
        self.data = {}
        self.lookup = {}
        self.jmespath_options = jmespath.Options(custom_functions=CustomFunctions())
        self.otm = None

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
                results = results + self.search(element, source)
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

            if "$root" in obj:
                return jmespath.search(obj["$root"], self.data, options=self.jmespath_options)

            if "$path" in obj:
                try:
                    return jmespath.search(obj["$path"], source, options=self.jmespath_options)
                except:
                    return []

            if "$format" in obj:
                return obj["$format"].format(**source)

            if "$catchall" in obj:
                #eturn jmespath.search(obj["$catchall"], self.data, options=self.jmespath_options)
                return self.search(obj["$catchall"], source)

            if "$search" in obj:
                results = []
                search_type = obj["$search"]["$type"]
                ref_value = jmespath.search(obj["$search"]["$ref"], source, options=self.jmespath_options)
                for refobj in self.otm.objects_by_type(search_type):
                    search_values = jmespath.search(obj["$search"]["$path"], refobj.source, options=self.jmespath_options)
                    if isinstance(search_values, list):
                        if ref_value in search_values:
                            results.append(refobj.id)
                    else:
                        if ref_value == search_values:
                            results.append(refobj.id) 
                return results

            return obj
