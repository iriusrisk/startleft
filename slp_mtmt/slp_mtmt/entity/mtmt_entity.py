is_component_stencil_list = ['StencilRectangle', 'StencilEllipse', 'StencilParallelLines']
is_trustzone_stencil_list = ['BorderBoundary', 'LineBoundary']
is_dataflow_stencil_list = ['Connector']


class MTMEntity:

    def __init__(self, source: dict):
        self.source = source

    @property
    def id(self):
        return self.source.get('Key')

    @property
    def type(self):
        return self.source.get('attrib', {}).get('type')

    @property
    def stencil_name(self):
        return self.source.get('Value', {}).get('Properties', {}).get('anyType')[0].get('DisplayName', {})

    @property
    def name(self):
        name = None
        for borderType in self.source.get('Value', {}).get('Properties', {}).get('anyType'):
            if borderType.get('DisplayName', '') == 'Name':
                name = borderType.get('Value', {}).get('text')
        return name
