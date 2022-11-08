is_component_stencil_list = ['StencilRectangle', 'StencilEllipse', 'StencilParallelLines']
is_trustzone_stencil_list = ['BorderBoundary', 'LineBoundary']


class MTMBorder:

    def __init__(self, source: dict):
        self.source = source

    @property
    def id(self):
        return self.source.get('Key')

    @property
    def name(self):
        name = None
        for borderType in self.source.get('Value', {}).get('Properties', {}).get('anyType'):
            if borderType.get('DisplayName', '') == 'Name':
                name = borderType.get('Value', {}).get('text')
        return name

    @property
    def type(self):
        return self.source.get('attrib', {}).get('type')

    @property
    def stencil_name(self):
        return self.source.get('Value', {}).get('Properties', {}).get('anyType')[0].get('DisplayName', {})

    @property
    def generic_type_id(self):
        return self.source.get('Value', {}).get('GenericTypeId')

    @property
    def height(self):
        return self.__extract_int_value('Height')

    @property
    def width(self):
        return self.__extract_int_value('Width')

    @property
    def left(self):
        return self.__extract_int_value('Left')

    @property
    def top(self):
        return self.__extract_int_value('Top')

    @property
    def properties(self):
        properties = {}
        for element in self.source.get('Value', {}).get('Properties', {}).get('anyType'):
            key = element.get('DisplayName')
            values = element.get('Value', {}).values()
            index = element.get('SelectedIndex', None)
            if key and len(values) > 0:
                value = list(values)[0]
                properties[key] = value[int(index)] if index else value
        return properties

    @property
    def is_component(self) -> bool:
        return self.type in is_component_stencil_list

    @property
    def is_trustzone(self) -> bool:
        return self.type in is_trustzone_stencil_list

    def __str__(self) -> str:
        return '{id: ' + str(self.id) + ', ' \
               + 'name: ' + str(self.name) + ', ' \
               + 'type: ' + str(self.type) + ', ' \
               + 'generic_type_id: ' + str(self.generic_type_id) + ', ' \
               + 'is_component: ' + str(self.is_component) + ', ' \
               + 'is_trustzone: ' + str(self.is_trustzone) + ', ' \
               + 'properties: ' + str(self.properties) + '}'

    def __extract_value(self, key):
        return self.source.get('Value').get(key)

    def __extract_int_value(self, key):
        return int(self.__extract_value(key))
