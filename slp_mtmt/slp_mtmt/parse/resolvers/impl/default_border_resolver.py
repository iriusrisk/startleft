from slp_mtmt.slp_mtmt.entity.mtmt_entity_border import MTMBorder
from slp_mtmt.slp_mtmt.parse.resolvers.border_type_resolver import BorderTypeResolver


class DefaultBorderResolver(BorderTypeResolver):

    def resolve(self, map_: dict, border: MTMBorder) -> str:
        return map_['type'] if 'type' in map_ else None
