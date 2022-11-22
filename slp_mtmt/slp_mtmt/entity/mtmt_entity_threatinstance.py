class MTMThreat:
    def __init__(self, source: dict):
        self.__thread_instance = source.get('Value')

        self.__properties = {}
        for element in self.__thread_instance.get('Properties').get('KeyValueOfstringstring'):
            key = element.get('Key')
            value = element.get('Value')
            self.__properties[key] = value

    @property
    def dataflow_id(self):
        return self.__thread_instance.get('FlowGuid')

    @property
    def source_component_id(self):
        return self.__thread_instance.get('SourceGuid')

    @property
    def destination_component_id(self):
        return self.__thread_instance.get('TargetGuid')

    @property
    def id(self):
        return self.__thread_instance.get('Id')

    @property
    def threat_priority(self):
        return self.__thread_instance.get('Priority')

    @property
    def threat_state(self):
        return self.__thread_instance.get('State')

    @property
    def justification(self):
        return self.__thread_instance.get('StateInformation')

    @property
    def title(self):
        return self.__properties.get('Title')

    @property
    def threat_category(self):
        return self.__properties.get('UserThreatCategory')

    @property
    def short_description(self):
        return self.__properties.get('UserThreatShortDescription')

    @property
    def long_description(self):
        return self.__properties.get('UserThreatDescription')

    @property
    def possible_mitigations(self):
        return self.__properties.get('PossibleMitigations')

    @property
    def steps(self):
        return self.__properties.get('Steps')

    @property
    def mitigation_effort(self):
        return self.__properties.get('Effort')

    @property
    def from_azure_template(self):
        return 'PossibleMitigations' in self.__properties and 'Steps' in self.__properties

    def __str__(self) -> str:
        return '{' \
                'id: ' + str(self.id) + ', ' + \
                'title: ' + str(self.title) + ', ' + \
                'threat_state: ' + str(self.threat_state) + ', ' + \
                'threat_priority: ' + str(self.threat_priority) + ', ' + \
                'threat_category: ' + str(self.threat_category) + ', ' + \
                'short_description: ' + str(self.short_description) + ', ' + \
                'destination_component_id: ' + str(self.destination_component_id) + \
                'from_azure_template: ' + str(self.from_azure_template) + \
               '}'
