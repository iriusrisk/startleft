from slp_mtmt.slp_mtmt.entity.mtmt_entity_border import MTMBorder
from slp_mtmt.slp_mtmt.parse.resolvers.border_type_resolver import BorderTypeResolver
from slp_mtmt.slp_mtmt.parse.resolvers.resolvers import get_type_resolver


class TestDefaultResolver:

    def test_common_components(self):
        # GIVEN The mapping element
        map_ = {'label': 'ADFS', 'type': 'active-directory'}

        # AND the resolver
        resolver: BorderTypeResolver = get_type_resolver('default')

        # WHEN we resolve the Mobile Client type
        type_ = resolver.resolve(map_, MTMBorder({}))

        # THEN validate
        assert type_ == 'active-directory'

    def test_wrong_map(self):
        # GIVEN The mapping element empty
        map_ = {}

        # AND the resolver
        resolver: BorderTypeResolver = get_type_resolver('default')

        # WHEN we resolve the Mobile Client type
        type_ = resolver.resolve(map_, MTMBorder({}))

        # THEN validate
        assert not type_
