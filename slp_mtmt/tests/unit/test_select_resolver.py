from pytest import mark

from slp_mtmt.slp_mtmt.entity.mtmt_entity_border import MTMBorder
from slp_mtmt.slp_mtmt.parse.resolvers.border_type_resolver import BorderTypeResolver
from slp_mtmt.slp_mtmt.parse.resolvers.resolvers import get_type_resolver


class TestSelectResolver:

    @mark.parametrize('selection,expected', [('3', 'android-device-client'), ('4', 'ios-device-client')])
    def test_mobile_client(self, selection, expected):
        # GIVEN The mapping element
        map_ = {'label': 'Mobile Client',
                'key': 'Mobile Client Technologies',
                'values': [
                    {'value': 'Android', 'type': 'android-device-client'},
                    {'value': 'iOS', 'type': 'ios-device-client'}
                ]}

        # AND the MTMBorder
        mtmt_source = {'Key': '6183b7fa-eba5-4bf8-a0af-c3e30d144a10',
                       'Value': {'Properties': {'anyType': [
                           {'DisplayName': 'Mobile Client Technologies', 'Value': {
                               'string': ['Select', 'Generic', 'Xamarin', 'Android',
                                          'iOS', 'Windows Phone']},
                            'SelectedIndex': selection}], }, },
                       'attrib': {'Id': 'i5', 'type': 'StencilRectangle'}}
        border = MTMBorder(mtmt_source)

        # AND the resolver
        resolver: BorderTypeResolver = get_type_resolver('Mobile Client')

        # WHEN we resolve the Mobile Client type
        type_ = resolver.resolve(map_, border)

        # THEN validate
        assert type_ == expected

    def test_wrong_map(self):
        # GIVEN The mapping element empty
        map_ = {}

        # AND the MTMBorder
        mtmt_source = {'Key': '6183b7fa-eba5-4bf8-a0af-c3e30d144a10',
                       'Value': {'Properties': {'anyType': [
                           {'DisplayName': 'Mobile Client Technologies', 'Value': {
                               'string': ['Select', 'Generic', 'Xamarin', 'Android',
                                          'iOS', 'Windows Phone']},
                            'SelectedIndex': '3'}], }, },
                       'attrib': {'Id': 'i5', 'type': 'StencilRectangle'}}
        border = MTMBorder(mtmt_source)

        # AND the resolver
        resolver: BorderTypeResolver = get_type_resolver('Mobile Client')

        # WHEN we resolve the Mobile Client type
        type_ = resolver.resolve(map_, border)

        # THEN validate
        assert not type_

    def test_wrong_mtmt(self):
        # GIVEN The mapping element
        map_ = {'label': 'Mobile Client',
                'key': 'Mobile Client Technologies',
                'values': [
                    {'value': 'Android', 'type': 'android-device-client'},
                    {'value': 'iOS', 'type': 'ios-device-client'}
                ]}

        # AND the MTMBorder empty
        mtmt_source = {}
        border = MTMBorder(mtmt_source)

        # AND the resolver
        resolver: BorderTypeResolver = get_type_resolver('Mobile Client')

        # WHEN we resolve the Mobile Client type
        type_ = resolver.resolve(map_, border)

        # THEN validate
        assert not type_
