from slp_tf.slp_tf.parse.mapping.search.functions.tf_custom_mapping_functions import root, skip, parent, singleton, \
    catchall, hub, ip, lookup, path, format, find_first, number_of_sources, module
from slp_tf.slp_tf.parse.mapping.search.functions.tf_query_mapping_functions import query


class MappingFunctionSelector:
    """
    Selector that return a given Mapping Function for the $source component mapping configuration
    """

    def __init__(self):
        self.config = {
            "$root": root,
            "$skip": skip,
            "$parent": parent,
            "$singleton": singleton,
            "$catchall": catchall,
            "$hub": hub,
            "$ip": ip,
            "$lookup": lookup,
            "$path": path,
            "$format": format,
            "$findFirst": find_first,
            "$numberOfSources": number_of_sources,
            "$type": query,
            "$name": query,
            "$props": query,
            "$module": module,
        }

    def get(self, obj):
        for key in obj:
            if elem := self.config.get(key, None):
                return elem
