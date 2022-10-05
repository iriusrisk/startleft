from slp_mtmt.slp_mtmt.entity.mtmt_entity_line import MTMLine
from slp_mtmt.slp_mtmt.tm7_to_json import Tm7ToJson
from slp_mtmt.tests.resources import test_resource_paths


def extract_lines(filepath):
    with open(filepath, 'r') as file:
        xml = file.read()
    json = Tm7ToJson(xml).to_json()
    lines = []
    for line in json['ThreatModel']['DrawingSurfaceList']['DrawingSurfaceModel']['Lines']['KeyValueOfguidanyType']:
        lines.append(MTMLine(line))
    return lines


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
        # GIVEN the lines from MTMT file
        lines = extract_lines(test_resource_paths.model_mtmt_with_lines)

        # THEN the result is as expected for all line data
        assert len(lines) == 3
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

    def test_mtmt_line_connector(self):
        # GIVEN the lines from MTMT file
        lines = extract_lines(test_resource_paths.model_mtmt_mvp)

        # THEN the result is as expected for all line data
        assert len(lines) == 6

        line = lines[0]
        assert line.id == 'eb072144-af37-4b75-b46b-b78111850d3e'
        assert line.description == 'Request'
        assert line.type == 'Connector'
        assert line.is_dataflow
        assert not line.is_trustzone
        assert line.name == 'PSQL Request'
        assert line.source_guid == '5d15323e-3729-4694-87b1-181c90af5045'
        assert line.target_guid == '53245f54-0656-4ede-a393-357aeaa2e20f'

        line = lines[1]
        assert line.id == '36091fd8-dba8-424e-a3cd-784ea6bcb9e0'
        assert line.description == 'Response'
        assert line.type == 'Connector'
        assert line.is_dataflow
        assert not line.is_trustzone
        assert line.name == 'PSQL Response'
        assert line.source_guid == '53245f54-0656-4ede-a393-357aeaa2e20f'
        assert line.target_guid == '5d15323e-3729-4694-87b1-181c90af5045'

        line = lines[2]
        assert line.id == 'f5fe3c6e-e10b-4252-a4aa-4ec6108c96a6'
        assert line.description == 'Request'
        assert line.type == 'Connector'
        assert line.is_dataflow
        assert not line.is_trustzone
        assert line.name == 'File Request'
        assert line.source_guid == '5d15323e-3729-4694-87b1-181c90af5045'
        assert line.target_guid == '91882aca-8249-49a7-96f0-164b68411b48'

        line = lines[3]
        assert line.id == 'f894ed9d-d1c3-42b7-9010-34274bf01c84'
        assert line.description == 'Response'
        assert line.type == 'Connector'
        assert line.is_dataflow
        assert not line.is_trustzone
        assert line.name == 'File Response'
        assert line.source_guid == '5d15323e-3729-4694-87b1-181c90af5045'
        assert line.target_guid == '91882aca-8249-49a7-96f0-164b68411b48'

        line = lines[4]
        assert line.id == '9840bcdf-c444-437d-8289-d5468f41b0db'
        assert line.description == 'Request'
        assert line.type == 'Connector'
        assert line.is_dataflow
        assert not line.is_trustzone
        assert line.name == 'API Request'
        assert line.source_guid == '6183b7fa-eba5-4bf8-a0af-c3e30d144a10'
        assert line.target_guid == '5d15323e-3729-4694-87b1-181c90af5045'

        line = lines[5]
        assert line.id == 'bf3d1783-c7c8-43dd-bfa4-efafeac1fe14'
        assert line.description == 'Response'
        assert line.type == 'Connector'
        assert line.is_dataflow
        assert not line.is_trustzone
        assert line.name == 'API Response'
        assert line.source_guid == '6183b7fa-eba5-4bf8-a0af-c3e30d144a10'
        assert line.target_guid == '5d15323e-3729-4694-87b1-181c90af5045'
