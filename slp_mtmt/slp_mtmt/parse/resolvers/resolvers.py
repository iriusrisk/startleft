from slp_mtmt.slp_mtmt.parse.resolvers.impl.default_border_resolver import DefaultBorderResolver
from slp_mtmt.slp_mtmt.parse.resolvers.impl.select_resolver import SelectBorderTypeResolver

resolvers_map: dict = {
    'default': DefaultBorderResolver(),
    'Mobile Client': SelectBorderTypeResolver()
}


def get_type_resolver(name):
    if name in resolvers_map:
        return resolvers_map[name]
    return resolvers_map['default']
