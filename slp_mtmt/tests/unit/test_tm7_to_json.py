from unittest import TestCase

from slp_mtmt.slp_mtmt.tm7_to_json import Tm7ToJson
from slp_mtmt.tests.resources import test_resource_paths


class TestTm7ToJson(TestCase):

    def test_to_json(self):
        # GIVEN the source MTMT data
        with open(test_resource_paths.model_mtmt_source_file, 'r') as f:
            xml = f.read()

        # AND the parser
        parser = Tm7ToJson(xml)

        # WHEN we convert to json
        json_ = parser.to_json()

        # THEN validate the threat model
        assert len(json_) == 1
        model_ = json_['ThreatModel']
        assert len(model_) == 9
        list_ = model_['DrawingSurfaceList']
        assert len(list_) == 1
        surface_model_ = list_['DrawingSurfaceModel']
        assert len(surface_model_) == 8
        borders_ = surface_model_['Borders']
        assert len(borders_) == 1
        types = borders_['KeyValueOfguidanyType']
        assert len(types) == 9
        current_type = types[0]
        assert current_type['Key'] == '294a595a-174d-452c-b38d-9c434f7f5bac'
        assert current_type['Value']['GenericTypeId'] == 'c8bba3ee-9cdc-426f-89dd-0cea09ba72e8'
        assert current_type['Value']['Guid'] == current_type['Key']
        assert current_type['Value']['Properties']['anyType'][0]['DisplayName'] == 'MCU'
        assert current_type['Value']['Properties']['anyType'][0]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][0]['Value'] == {}
        assert current_type['Value']['Properties']['anyType'][1]['DisplayName'] == 'Name'
        assert current_type['Value']['Properties']['anyType'][1]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][1]['Value']['text'] == 'My_MCU'
        current_type = types[1]
        assert current_type['Key'] == '436f7fa6-8555-4b73-9346-679874c650e7'
        assert current_type['Value']['GenericTypeId'] == 'c8bba3ee-9cdc-426f-89dd-0cea09ba72e8'
        assert current_type['Value']['Guid'] == current_type['Key']
        assert current_type['Value']['Properties']['anyType'][0]['DisplayName'] == 'Memory'
        assert current_type['Value']['Properties']['anyType'][0]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][0]['Value'] == {}
        assert current_type['Value']['Properties']['anyType'][1]['DisplayName'] == 'Name'
        assert current_type['Value']['Properties']['anyType'][1]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][1]['Value']['text'] == 'SD card'
        current_type = types[2]
        assert current_type['Key'] == '241852d1-a5a7-4756-86d5-b400703b6614'
        assert current_type['Value']['GenericTypeId'] == '06836650-88ef-4421-a2d8-88cb8befbff0'
        assert current_type['Value']['Guid'] == current_type['Key']
        assert current_type['Value']['Properties']['anyType'][0]['DisplayName'] == 'Device Physical Boundary'
        assert current_type['Value']['Properties']['anyType'][0]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][0]['Value'] == {}
        assert current_type['Value']['Properties']['anyType'][1]['DisplayName'] == 'Name'
        assert current_type['Value']['Properties']['anyType'][1]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][1]['Value']['text'] == 'Device Physical Boundary'
        current_type = types[3]
        assert current_type['Key'] == '5b0bab1d-89c8-499d-b9aa-a5d19652aa5f'
        assert current_type['Value']['GenericTypeId'] == '8db306cc-f8f5-4c07-8be2-48e2a0af38aa'
        assert current_type['Value']['Guid'] == current_type['Key']
        assert current_type['Value']['Properties']['anyType'][0]['DisplayName'] == 'Phone'
        assert current_type['Value']['Properties']['anyType'][0]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][0]['Value'] == {}
        assert current_type['Value']['Properties']['anyType'][1]['DisplayName'] == 'Name'
        assert current_type['Value']['Properties']['anyType'][1]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][1]['Value']['text'] == 'Phone'
        current_type = types[4]
        assert current_type['Key'] == '26418f1e-db19-41ad-9157-1ea2cebbaec6'
        assert current_type['Value']['GenericTypeId'] == '06836650-88ef-4421-a2d8-88cb8befbff0'
        assert current_type['Value']['Guid'] == current_type['Key']
        assert current_type['Value']['Properties']['anyType'][0]['DisplayName'] == 'SoC Boundary'
        assert current_type['Value']['Properties']['anyType'][0]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][0]['Value'] == {}
        assert current_type['Value']['Properties']['anyType'][1]['DisplayName'] == 'Name'
        assert current_type['Value']['Properties']['anyType'][1]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][1]['Value']['text'] == 'SoC Boundary'
        current_type = types[5]
        assert current_type['Key'] == '8688c03a-1943-420c-8411-038d652220ca'
        assert current_type['Value']['GenericTypeId'] == '06836650-88ef-4421-a2d8-88cb8befbff0'
        assert current_type['Value']['Guid'] == current_type['Key']
        assert current_type['Value']['Properties']['anyType'][0]['DisplayName'] == 'Local Network Boundary'
        assert current_type['Value']['Properties']['anyType'][0]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][0]['Value'] == {}
        assert current_type['Value']['Properties']['anyType'][1]['DisplayName'] == 'Name'
        assert current_type['Value']['Properties']['anyType'][1]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][1]['Value']['text'] == 'Local Network Boundary'
        current_type = types[6]
        assert current_type['Key'] == '158ab95e-f8d0-48d7-84f8-4c57ed40a9f4'
        assert current_type['Value']['GenericTypeId'] == '8db306cc-f8f5-4c07-8be2-48e2a0af38aa'
        assert current_type['Value']['Guid'] == current_type['Key']
        assert current_type['Value']['Properties']['anyType'][0]['DisplayName'] == 'Server'
        assert current_type['Value']['Properties']['anyType'][0]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][0]['Value'] == {}
        assert current_type['Value']['Properties']['anyType'][1]['DisplayName'] == 'Name'
        assert current_type['Value']['Properties']['anyType'][1]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][1]['Value']['text'] == 'Server'
        current_type = types[7]
        assert current_type['Key'] == '086f799f-e4f4-4c70-8f82-e1fd1212e22b'
        assert current_type['Value']['GenericTypeId'] == '06836650-88ef-4421-a2d8-88cb8befbff0'
        assert current_type['Value']['Guid'] == current_type['Key']
        assert current_type['Value']['Properties']['anyType'][0]['DisplayName'] == 'Company Internet Boundary'
        assert current_type['Value']['Properties']['anyType'][0]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][0]['Value'] == {}
        assert current_type['Value']['Properties']['anyType'][1]['DisplayName'] == 'Name'
        assert current_type['Value']['Properties']['anyType'][1]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][1]['Value']['text'] == 'Company Internet Boundary'
        current_type = types[8]
        assert current_type['Key'] == 'ca3c7bc2-377f-471f-a45f-a78d511a4184'
        assert current_type['Value']['GenericTypeId'] == 'dd163aaf-713b-46df-bc66-4ace6c033067'
        assert current_type['Value']['Guid'] == current_type['Key']
        assert current_type['Value']['Properties']['anyType'][0]['DisplayName'] == 'Attacker'
        assert current_type['Value']['Properties']['anyType'][0]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][0]['Value'] == {}
        assert current_type['Value']['Properties']['anyType'][1]['DisplayName'] == 'Name'
        assert current_type['Value']['Properties']['anyType'][1]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][1]['Value']['text'] == 'Attacker'
        lines = surface_model_['Lines']
        types = lines['KeyValueOfguidanyType']
        assert len(types) == 8
        current_type = types[0]
        assert current_type['Key'] == '8ee98acb-b1b9-44b4-9bdb-ee129fdb072b'
        assert current_type['Value']['GenericTypeId'] == '480937d2-d4f4-4af0-8282-4cd42bc5b75e'
        assert current_type['Value']['Guid'] == current_type['Key']
        assert current_type['Value']['Properties']['anyType'][0]['DisplayName'] == 'Local Digital Communication'
        assert current_type['Value']['Properties']['anyType'][0]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][0]['Value'] == {}
        assert current_type['Value']['Properties']['anyType'][1]['DisplayName'] == 'Name'
        assert current_type['Value']['Properties']['anyType'][1]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][1]['Value']['text'] == 'SD SPI Out'
        current_type = types[1]
        assert current_type['Key'] == '12acd5a9-0e2d-4833-a28a-bf7ee8e694ce'
        assert current_type['Value']['GenericTypeId'] == '480937d2-d4f4-4af0-8282-4cd42bc5b75e'
        assert current_type['Value']['Guid'] == current_type['Key']
        assert current_type['Value']['Properties']['anyType'][0]['DisplayName'] == 'Local Digital Communication'
        assert current_type['Value']['Properties']['anyType'][0]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][0]['Value'] == {}
        assert current_type['Value']['Properties']['anyType'][1]['DisplayName'] == 'Name'
        assert current_type['Value']['Properties']['anyType'][1]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][1]['Value']['text'] == 'SD SPI In'
        current_type = types[2]
        assert current_type['Key'] == '4ecea2e4-18da-45d9-9373-a0112766af32'
        assert current_type['Value']['GenericTypeId'] == '480937d2-d4f4-4af0-8282-4cd42bc5b75e'
        assert current_type['Value']['Guid'] == current_type['Key']
        assert current_type['Value']['Properties']['anyType'][0]['DisplayName'] == 'Wireless Networks'
        assert current_type['Value']['Properties']['anyType'][0]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][0]['Value'] == {}
        assert current_type['Value']['Properties']['anyType'][1]['DisplayName'] == 'Name'
        assert current_type['Value']['Properties']['anyType'][1]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][1]['Value']['text'] == 'HTTPS Out'
        current_type = types[3]
        assert current_type['Key'] == '12cd91c3-e9d9-4523-aa7b-3aab3585249f'
        assert current_type['Value']['GenericTypeId'] == '480937d2-d4f4-4af0-8282-4cd42bc5b75e'
        assert current_type['Value']['Guid'] == current_type['Key']
        assert current_type['Value']['Properties']['anyType'][0]['DisplayName'] == 'Wireless Networks'
        assert current_type['Value']['Properties']['anyType'][0]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][0]['Value'] == {}
        assert current_type['Value']['Properties']['anyType'][1]['DisplayName'] == 'Name'
        assert current_type['Value']['Properties']['anyType'][1]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][1]['Value']['text'] == 'HTTPS In'
        current_type = types[4]
        assert current_type['Key'] == '7760688a-3514-4d51-9b4e-8f4e336b2c33'
        assert current_type['Value']['GenericTypeId'] == '480937d2-d4f4-4af0-8282-4cd42bc5b75e'
        assert current_type['Value']['Guid'] == current_type['Key']
        assert current_type['Value']['Properties']['anyType'][0]['DisplayName'] == 'Local Wireless'
        assert current_type['Value']['Properties']['anyType'][0]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][0]['Value'] == {}
        assert current_type['Value']['Properties']['anyType'][1]['DisplayName'] == 'Name'
        assert current_type['Value']['Properties']['anyType'][1]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][1]['Value']['text'] == 'BLE Out'
        current_type = types[5]
        assert current_type['Key'] == '30eea514-cce9-4a5b-a8ff-a2301097b394'
        assert current_type['Value']['GenericTypeId'] == '480937d2-d4f4-4af0-8282-4cd42bc5b75e'
        assert current_type['Value']['Guid'] == current_type['Key']
        assert current_type['Value']['Properties']['anyType'][0]['DisplayName'] == 'Local Wireless'
        assert current_type['Value']['Properties']['anyType'][0]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][0]['Value'] == {}
        assert current_type['Value']['Properties']['anyType'][1]['DisplayName'] == 'Name'
        assert current_type['Value']['Properties']['anyType'][1]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][1]['Value']['text'] == 'BLE In'
        current_type = types[6]
        assert current_type['Key'] == '2623e7d0-e277-46ad-8d13-6e47d10e3d35'
        assert current_type['Value']['GenericTypeId'] == '480937d2-d4f4-4af0-8282-4cd42bc5b75e'
        assert current_type['Value']['Guid'] == current_type['Key']
        assert current_type['Value']['Properties']['anyType'][0]['DisplayName'] == 'Local Digital Communication'
        assert current_type['Value']['Properties']['anyType'][0]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][0]['Value'] == {}
        assert current_type['Value']['Properties']['anyType'][1]['DisplayName'] == 'Name'
        assert current_type['Value']['Properties']['anyType'][1]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][1]['Value']['text'] == 'Attacker Out'
        current_type = types[7]
        assert current_type['Key'] == 'bd0b560e-339f-4b24-9e5d-1c3c50b4c6bc'
        assert current_type['Value']['GenericTypeId'] == '480937d2-d4f4-4af0-8282-4cd42bc5b75e'
        assert current_type['Value']['Guid'] == current_type['Key']
        assert current_type['Value']['Properties']['anyType'][0]['DisplayName'] == 'Local Digital Communication'
        assert current_type['Value']['Properties']['anyType'][0]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][0]['Value'] == {}
        assert current_type['Value']['Properties']['anyType'][1]['DisplayName'] == 'Name'
        assert current_type['Value']['Properties']['anyType'][1]['Name'] is None
        assert current_type['Value']['Properties']['anyType'][1]['Value']['text'] == 'Attacker In'
        meta_info = model_['MetaInformation']
        assert len(meta_info) == 7
        assert meta_info['Assumptions'] == 'None'
        assert meta_info['Contributors'] == 'Tyler M'
        assert meta_info['ExternalDependencies'] == 'None'
        assert meta_info['HighLevelSystemDescription'] == 'Test model to test out different electrical components'
        assert meta_info['Owner'] == 'Tyler M'
        assert meta_info['Reviewer'] == 'Tyler M'
        assert meta_info['ThreatModelName'] == 'TestSystem'
        notes = model_['Notes']
        assert len(notes) == 1
        note = notes['Note']
        assert len(note) == 3
        threat_instance = model_['ThreatInstances']
        threats = threat_instance['KeyValueOfstringThreatpc_P0_PhOB']
        assert len(threats) == 10
        current_threat = threats[0]
        assert current_threat['Key'] == '19c4f63f-dd2f-4b71-bca2-46937ce7178b5b0bab1d-89c8-499d-b9aa' \
                                        '-a5d19652aa5f4ecea2e4-18da-45d9-9373-a0112766af32158ab95e-f8d0-48d7-84f8' \
                                        '-4c57ed40a9f4'
        assert current_threat['Value']['DrawingSurfaceGuid'] == 'd81aacfd-973b-47f1-b424-dafd887d09c1'
        assert current_threat['Value']['FlowGuid'] == '4ecea2e4-18da-45d9-9373-a0112766af32'
        assert current_threat['Value']['Id'] == '10'
        assert current_threat['Value']['InteractionKey'] == '5b0bab1d-89c8-499d-b9aa-a5d19652aa5f:4ecea2e4-18da-45d9' \
                                                            '-9373-a0112766af32:158ab95e-f8d0-48d7-84f8-4c57ed40a9f4'
        assert current_threat['Value']['InteractionString'] == {}
        assert current_threat['Value']['ModifiedAt'] == '0001-01-01T00:00:00'
        assert current_threat['Value']['Priority'] == 'highest'
        assert len(current_threat['Value']['Properties']) == 1
        assert len(current_threat['Value']['Properties']['KeyValueOfstringstring']) == 15
        assert current_threat['Value']['SourceGuid'] == '5b0bab1d-89c8-499d-b9aa-a5d19652aa5f'
        assert current_threat['Value']['State'] == 'AutoGenerated'
        assert current_threat['Value']['StateInformation'] == {}
        assert current_threat['Value']['TargetGuid'] == '158ab95e-f8d0-48d7-84f8-4c57ed40a9f4'
        assert current_threat['Value']['Title'] == {}
        assert current_threat['Value']['TypeId'] == '19c4f63f-dd2f-4b71-bca2-46937ce7178b'
        assert current_threat['Value']['Upgraded'] == 'false'
        assert current_threat['Value']['UserThreatCategory'] == {}
        assert current_threat['Value']['UserThreatDescription'] == {}
        assert current_threat['Value']['UserThreatShortDescription'] == {}
        assert current_threat['Value']['Wide'] == 'false'
        current_threat = threats[1]
        assert current_threat['Key'] == 'f05a81cf-b6a1-4ccf-94fc-3ad2af411ecd294a595a-174d-452c-b38d' \
                                        '-9c434f7f5bac7760688a-3514-4d51-9b4e-8f4e336b2c335b0bab1d-89c8-499d-b9aa' \
                                        '-a5d19652aa5f'
        assert current_threat['Value']['DrawingSurfaceGuid'] == 'd81aacfd-973b-47f1-b424-dafd887d09c1'
        assert current_threat['Value']['FlowGuid'] == '7760688a-3514-4d51-9b4e-8f4e336b2c33'
        assert current_threat['Value']['Id'] == '1'
        assert current_threat['Value']['InteractionKey'] == '294a595a-174d-452c-b38d-9c434f7f5bac:7760688a-3514-4d51' \
                                                            '-9b4e-8f4e336b2c33:5b0bab1d-89c8-499d-b9aa-a5d19652aa5f'
        assert current_threat['Value']['InteractionString'] == {}
        assert current_threat['Value']['ModifiedAt'] == '2021-02-18T13:51:48.7662941-07:00'
        assert current_threat['Value']['Priority'] == 'highest'
        assert len(current_threat['Value']['Properties']) == 1
        assert len(current_threat['Value']['Properties']['KeyValueOfstringstring']) == 15
        assert current_threat['Value']['SourceGuid'] == '294a595a-174d-452c-b38d-9c434f7f5bac'
        assert current_threat['Value']['State'] == 'AutoGenerated'
        assert current_threat['Value']['StateInformation'] == {}
        assert current_threat['Value']['TargetGuid'] == '5b0bab1d-89c8-499d-b9aa-a5d19652aa5f'
        assert current_threat['Value']['Title'] == {}
        assert current_threat['Value']['TypeId'] == 'f05a81cf-b6a1-4ccf-94fc-3ad2af411ecd'
        assert current_threat['Value']['Upgraded'] == 'false'
        assert current_threat['Value']['UserThreatCategory'] == {}
        assert current_threat['Value']['UserThreatDescription'] == {}
        assert current_threat['Value']['UserThreatShortDescription'] == {}
        assert current_threat['Value']['Wide'] == 'false'
        knowlegde_base = model_['KnowledgeBase']
        assert len(knowlegde_base) == 6
        gen_elements = knowlegde_base['GenericElements']
        assert len(gen_elements) == 1
        types = gen_elements['ElementType']
        assert len(types) == 7
        current_type = types[0]
        assert current_type['IsExtension'] == 'false'
        assert current_type['Attributes'] is None
        assert current_type['AvailableToBaseModels'] is None
        assert current_type['Behavior'] == {}
        assert current_type['Description'] is None
        assert current_type['Hidden'] == 'false'
        assert current_type['Id'] == 'dd163aaf-713b-46df-bc66-4ace6c033067'
        assert current_type['ImageStream'] == {}
        assert current_type['Name'] == 'Generic Interaction'
        assert current_type['ParentId'] == 'ROOT'
        assert current_type['Representation'] == 'Ellipse'
