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
        return self.__thread_instance.get('FlowGuid') or None

    @property
    def source_component_id(self):
        return self.__thread_instance.get('SourceGuid') or None

    @property
    def destination_component_id(self):
        return self.__thread_instance.get('TargetGuid') or None

    @property
    def id(self):
        return self.__thread_instance.get('Id') or None

    @property
    def threat_priority(self):
        return self.__thread_instance.get('Priority') or None

    @property
    def threat_state(self):
        return self.__thread_instance.get('State') or None

    @property
    def justification(self):
        return self.__thread_instance.get('StateInformation') or None

    @property
    def title(self):
        return self.__properties.get('Title') or None

    @property
    def threat_category(self):
        return self.__properties.get('UserThreatCategory') or None

    @property
    def short_description(self):
        return self.__properties.get('UserThreatShortDescription') or None

    @property
    def long_description(self):
        return self.__properties.get('UserThreatDescription') or None

    @property
    def possible_mitigations(self):
        return self.__properties.get('PossibleMitigations') or None

    @property
    def steps(self):
        return self.__properties.get('Steps') or None

    @property
    def mitigation_effort(self):
        return self.__properties.get('Effort') or None

    @property
    def from_azure_template(self):
        return 'PossibleMitigations' in self.__properties

    def __str__(self) -> str:
        return '{' \
                'id: ' + str(self.id) + ', ' + \
                'title: ' + str(self.title) + ', ' + \
                'threat_state: ' + str(self.threat_state) + ', ' + \
                'threat_category: ' + str(self.threat_category) + ', ' + \
                'destination_component_id: ' + str(self.destination_component_id) + \
                'from_azure_template: ' + str(self.from_azure_template) + \
               '}'
