from slp_mtmt.slp_mtmt.entity.mtmt_entity import MTMEntity, is_dataflow_stencil_list, is_trustzone_stencil_list


class MTMLine(MTMEntity):

    def __init__(self, source: dict):
        super().__init__(source)

    @property
    def description(self):
        return self.__get_first_property()

    @property
    def is_trustzone(self) -> bool:
        return self.type in is_trustzone_stencil_list

    @property
    def is_dataflow(self) -> bool:
        return self.type in is_dataflow_stencil_list

    @property
    def source_guid(self):
        return self.__extract_value('SourceGuid')

    @property
    def target_guid(self):
        return self.__extract_value('TargetGuid')

    @property
    def handle_x(self):
        return self.__extract_int_value('HandleX')

    @property
    def handle_y(self):
        return self.__extract_int_value('HandleY')

    @property
    def source_x(self):
        return self.__extract_int_value('SourceX')

    @property
    def source_y(self):
        return self.__extract_int_value('SourceY')

    @property
    def target_x(self):
        return self.__extract_int_value('TargetX')

    @property
    def target_y(self):
        return self.__extract_int_value('TargetY')

    @property
    def coordinates(self):
        return self.handle_x, self.handle_y, self.source_x, self.source_y, self.target_x, self.target_y

    def __extract_value(self, key):
        return self.source.get('Value').get(key)

    def __extract_int_value(self, key):
        return int(self.__extract_value(key))

    @property
    def properties(self):
        properties = {}
        for _property in self.source.get('Value', {}).get('Properties', {}).get('anyType'):
            key = _property.get('DisplayName')
            values = _property.get('Value')
            if key:
                if len(values) > 0:
                    index = _property.get('SelectedIndex')
                    value = list(values.values())[0]
                    properties[key] = value[int(index)] if index and type(value) is list else value
                else:
                    properties[key] = {}
        return properties

    def __get_first_property(self):
        return list(self.properties.keys())[0]

    def __str__(self) -> str:
        return '{id: ' + str(self.id) + ', ' \
               + 'name: ' + str(self.name) + ', ' \
               + 'description: ' + str(self.description) + ', ' \
               + 'type: ' + str(self.type) + ', ' \
               + 'is_trustzone: ' + str(self.is_trustzone) + ', ' \
               + 'is_dataflow: ' + str(self.is_dataflow) + ', ' \
               + 'source_guid: ' + str(self.source_guid) + ', ' \
               + 'target_guid: ' + str(self.target_guid) + ', ' \
               + 'properties: ' + str(self.properties) + '}'
