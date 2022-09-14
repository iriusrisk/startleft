from startleft.processors.mtmt.tm7_to_json import Tm7ToJson
from startleft.processors.mtmt.entity.mtmt_entity_line import MTMLine
from tests.resources import test_resource_paths


class TestMTMTLine:
    line_fields_expected_results = [
        {'id': '264aa048-3595-4d94-b7b4-53ac7f447c6a', 'name': 'SQL Server Replication',
         'description': 'TLS', 'type': 'Connector', 'is_trustzone': False, 'is_dataflow': True},
        {'id': 'c5c861dd-02be-4817-ab7f-bc6ded1ab80a', 'name': 'Internet Boundary',
         'description': 'Internet Boundary', 'type': 'LineBoundary', 'is_trustzone': True, 'is_dataflow': False},
        {'id': 'c5c861ff-02ge-4817-ab7f-bc6ded1cd90a', 'name': 'Test Boundary',
         'description': 'Test Boundary', 'type': 'LineBoundary', 'is_trustzone': True, 'is_dataflow': False}
    ]

    line_properties_expected_results = [
        {'TLS': {}, 'Name': 'SQL Server Replication', 'Dataflow Order': '0', 'Out Of Scope': 'false',
         'Reason For Out Of Scope': {}, 'Configurable Attributes': {}, 'access vector': 'Physical',
         'As Generic Communication': {}, 'has authentication': 'no'},
        {'Internet Boundary': {}, 'Name': 'Internet Boundary', 'Configurable Attributes': {},
         'As Generic Trust Line Boundary': {}},
        {'As Generic Trust Line Boundary': {}, 'Configurable Attributes': {}, 'Name': 'Test Boundary',
         'TLS Version': '1 3', 'Test Boundary': {}}
    ]

    def test_mtmt_line(self):
        # GIVEN the source MTMT data as XML
        with open(test_resource_paths.model_mtmt_with_lines, 'r') as file:
            xml = file.read()

        # WHEN we convert to json
        json = Tm7ToJson(xml).to_json()

        # AND build MTMTLine entities
        lines = []
        for line in json['ThreatModel']['DrawingSurfaceList']['DrawingSurfaceModel']['Lines']['KeyValueOfguidanyType']:
            lines.append(MTMLine(line))

        # THEN the result is as expected for all line data
        for index in range(0, len(lines)):
            current_line = lines[index]
            expected_fields = self.line_fields_expected_results[index]
            expected_properties = self.line_properties_expected_results[index]

            assert current_line.id == expected_fields['id']
            assert current_line.name == expected_fields['name']
            assert current_line.description == expected_fields['description']
            assert current_line.type == expected_fields['type']
            assert current_line.is_trustzone == expected_fields['is_trustzone']
            assert current_line.is_dataflow == expected_fields['is_dataflow']
            assert current_line.properties == expected_properties
