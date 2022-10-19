import logging

from slp_mtmt.slp_mtmt.entity.mtmt_entity_border import MTMBorder
from slp_mtmt.slp_mtmt.parse.resolvers.border_type_resolver import BorderTypeResolver

logger = logging.getLogger(__name__)


class SelectBorderTypeResolver(BorderTypeResolver):
    """
    Resolver for a MTMT Select such as:
        <b:DisplayName>Mobile Client Technologies</b:DisplayName>
        ...
            <b:Value i:type="a:ArrayOfstring">
                <a:string>Select</a:string>
                <a:string>Android</a:string>
                <a:string>iOS</a:string>
            </b:Value>
            <b:SelectedIndex>3</b:SelectedIndex>

    The structure of mapping should be such as:
            -  label: Mobile Client
               key: Mobile Client Technologies
               values:
                  - value: Android
                    type: android-device-client
                  - value: iOS
                    type: ios-device-client


    """

    def resolve(self, map_: dict, border: MTMBorder):
        try:
            key = map_['key']
            selection = border.properties[key]
            for pair in map_['values']:
                if pair['value'] == selection:
                    return pair['type']
        except (KeyError, TypeError) as e:
            logger.warning(f'Source format error: Unable to resolve otm type from border. Error: {e}')

        return None
