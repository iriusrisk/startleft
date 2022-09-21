is_trustzone_stencil_list = ['LineBoundary']
is_dataflow_stencil_list = ['Connector']


class MTMLine:

    def __init__(self, source: dict):
        self.source = source

    @property
    def id(self):
        return self.source.get('Key')

    @property
    def name(self):
        return self.properties.get('Name', self.__get_first_property())  # fallback is first property

    @property
    def description(self):
        return self.__get_first_property()

    @property
    def type(self):
        return self.source.get('attrib', {}).get('type')

    @property
    def is_trustzone(self) -> bool:
        return self.type in is_trustzone_stencil_list

    @property
    def is_dataflow(self) -> bool:
        return self.type in is_dataflow_stencil_list

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
               + 'properties: ' + str(self.properties) + '}'
