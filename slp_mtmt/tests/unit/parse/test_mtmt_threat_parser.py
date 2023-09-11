import pytest

from otm.otm.entity.component import Component
from otm.otm.entity.mitigation import Mitigation, MitigationInstance
from otm.otm.entity.threat import Threat, ThreatInstance
from slp_mtmt.slp_mtmt.entity.mtmt_entity_threatinstance import MTMThreat
from slp_mtmt.slp_mtmt.mtmt_entity import MTMT, MTMKnowledge
from slp_mtmt.slp_mtmt.parse.mtmt_threat_parser import MTMThreatParser, get_threat_description, \
    get_mitigation_description, remove_trailing_dot


def assert_threat(threat: Threat, json: dict):
    assert threat.json() == json


def assert_mitigation(mitigation: Mitigation, json: dict):
    assert mitigation.json() == json


class TestMTMThreatParser:
    threat = {
        "Value": {
            "Id": 30,
            "SourceGuid": "8668f6af-f5a0-47eb-ad27-ce8a7d16303b",
            "TargetGuid": "ff5f3e59-caa6-464c-8b3e-528d6a3dbfbb",
            "FlowGuid": "501a8a2a-19ad-49f1-8ff8-0740bc303214",
            "State": "Mitigated",
            "Priority": "High",
            "StateInformation": "",
            "Properties": {
                "KeyValueOfstringstring": [
                    {
                        "Key": "Title",
                        "Value": "Web Application Process Memory Tampered"
                    },
                    {
                        "Key": "UserThreatCategory",
                        "Value": "Tampering"
                    },
                    {
                        "Key": "UserThreatShortDescription",
                        "Value": "Tampering is the act of altering the bits. Tampering with a process involves changing bits in the running process."
                    },
                    {
                        "Key": "UserThreatDescription",
                        "Value": "If Web Application is given access to memory, such as shared memory or pointers, or is given the ability to control what Web Service executes (for example, passing back a function pointer.), then Web Application can tamper with Web Service. Consider if the function could work with less access to memory, such as passing data rather than pointers."
                    }
                ]

            }
        }
    }
    expected_otm_threat = {
        "name": "Web Application Process Memory Tampered",
        "id": 30,
        "categories": [
            "Tampering"
        ],
        "description": "If Web Application is given access to memory, such as shared memory or pointers, or is given the ability to control what Web Service executes (for example, passing back a function pointer.), then Web Application can tamper with Web Service",
        "risk": {
            "likelihood": 100,
            "impact": 100
        }
    }
    expected_otm_mitigation = {
        "name": "Consider if the function could work with less access to memory, such as passing data rather than pointers",
        "id": 30,
        "description": "Consider if the function could work with less access to memory, such as passing data rather than pointers",
        "riskReduction": 100
    }
    threat_azure = {
        "Value": {
            "Id": 30,
            "SourceGuid": "8668f6af-f5a0-47eb-ad27-ce8a7d16303b",
            "TargetGuid": "ff5f3e59-caa6-464c-8b3e-528d6a3dbfbb",
            "FlowGuid": "501a8a2a-19ad-49f1-8ff8-0740bc303214",
            "State": "Mitigated",
            "Priority": "High",
            "StateInformation": "",
            "Properties": {
                "KeyValueOfstringstring": [
                    {
                        "Key": "Title",
                        "Value": "An adversary may gain unauthorized access to Azure Data Factory (ingest) account in a subscription"
                    },
                    {
                        "Key": "UserThreatCategory",
                        "Value": "Elevation Of Privilege"
                    },
                    {
                        "Key": "UserThreatShortDescription",
                        "Value": "A user subject gains increased capability or privilege by taking advantage of an implementation bug."
                    },
                    {
                        "Key": "UserThreatDescription",
                        "Value": "An adversary may gain unauthorized access to Azure Data Factory (ingest) account in a subscription."
                    },
                    {
                        "Key": "PossibleMitigations",
                        "Value": 'Enable Role-Based Access Control (RBAC) to Azure storage account using Azure Resource Manager. Refer: &lt;a href="https://aka.ms/tmtauthz#rbac-azure-manager"&gt;https://aka.ms/tmtauthz#rbac-azure-manager&lt;/a&gt;'
                    },
                    {
                        "Key": "Steps",
                        "Value": "When you create a new storage account, you select a deployment model of Classic or Azure Resource Manager. The Classic model of creating resources in Azure only allows all-or-nothing access to the subscription, and in turn, the storage account. With the Azure Resource Manager model, you put the storage account in a resource group and control access to the management plane of that specific storage account using Azure Active Directory. For example, you can give specific users the ability to access the storage account keys, while other users can view information about the storage account, but cannot access the storage account keys."
                    },
                    {
                        "Key": "Effort",
                        "Value": "Low"
                    }
                ]

            }
        }
    }
    expected_otm_threat_azure = {
        "name": "An adversary may gain unauthorized access to Azure Data Factory (ingest) account in a subscription",
        "id": 30,
        "categories": [
            "Elevation Of Privilege"
        ],
        "description": "An adversary may gain unauthorized access to Azure Data Factory (ingest) account in a subscription",
        "risk": {
            "likelihood": 100,
            "impact": 100
        }
    }
    expected_otm_mitigation_azure = {
        "name": "Enable Role-Based Access Control (RBAC) to Azure storage account using Azure Resource Manager",
        "id": 30,
        "description": "When you create a new storage account, you select a deployment model of Classic or Azure Resource Manager. The Classic model of creating resources in Azure only allows all-or-nothing access to the subscription, and in turn, the storage account. With the Azure Resource Manager model, you put the storage account in a resource group and control access to the management plane of that specific storage account using Azure Active Directory. For example, you can give specific users the ability to access the storage account keys, while other users can view information about the storage account, but cannot access the storage account keys",
        "riskReduction": 100
    }
    threat_azure_without_steps = {
        "Value": {
            "Id": 30,
            "SourceGuid": "8668f6af-f5a0-47eb-ad27-ce8a7d16303b",
            "TargetGuid": "ff5f3e59-caa6-464c-8b3e-528d6a3dbfbb",
            "FlowGuid": "501a8a2a-19ad-49f1-8ff8-0740bc303214",
            "State": "Mitigated",
            "Priority": "High",
            "StateInformation": "",
            "Properties": {
                "KeyValueOfstringstring": [
                    {
                        "Key": "Title",
                        "Value": "An adversary may gain unauthorized access to Azure Data Factory (ingest) account in a subscription"
                    },
                    {
                        "Key": "UserThreatCategory",
                        "Value": "Elevation Of Privilege"
                    },
                    {
                        "Key": "UserThreatShortDescription",
                        "Value": "A user subject gains increased capability or privilege by taking advantage of an implementation bug."
                    },
                    {
                        "Key": "UserThreatDescription",
                        "Value": "An adversary may gain unauthorized access to Azure Data Factory (ingest) account in a subscription."
                    },
                    {
                        "Key": "PossibleMitigations",
                        "Value": 'Enable Role-Based Access Control (RBAC) to Azure storage account using Azure Resource Manager. Refer: &lt;a href="https://aka.ms/tmtauthz#rbac-azure-manager"&gt;https://aka.ms/tmtauthz#rbac-azure-manager&lt;/a&gt;'
                    },
                    {
                        "Key": "Effort",
                        "Value": "Low"
                    }
                ]

            }
        }
    }
    expected_otm_mitigation_azure_without_steps = {
        "name": "Enable Role-Based Access Control (RBAC) to Azure storage account using Azure Resource Manager",
        "id": 30,
        "description": 'Enable Role-Based Access Control (RBAC) to Azure storage account using Azure Resource Manager. Refer: &lt;a href="https://aka.ms/tmtauthz#rbac-azure-manager"&gt;https://aka.ms/tmtauthz#rbac-azure-manager&lt;/a&gt;',
        "riskReduction": 100
    }
    components = [
        Component(
            component_id="ff5f3e59-caa6-464c-8b3e-528d6a3dbfbb",
            name="Micro-Batch (Managed App)",
            component_type="web-application-server-side",
            parent="2ab4effa-40b7-4cd2-ba81-8247d29a6f2d",
            parent_type="trustZone",
            attributes={
                "Name": "Micro-Batch (Managed App)",
                "Out Of Scope": "false",
                "Isolation Level": "Not Selected",
                "Show Generic Process Threat": "Yes"
            }
        )
    ]
    expected_component = {
        "id": "ff5f3e59-caa6-464c-8b3e-528d6a3dbfbb",
        "name": "Micro-Batch (Managed App)",
        "type": "web-application-server-side",
        "parent": {
            "trustZone": "2ab4effa-40b7-4cd2-ba81-8247d29a6f2d"
        },
        "attributes": {
            "Name": "Micro-Batch (Managed App)",
            "Out Of Scope": "false",
            "Isolation Level": "Not Selected",
            "Show Generic Process Threat": "Yes"
        },
        "threats": [ThreatInstance(30, "Mitigated", [MitigationInstance(30, "IMPLEMENTED")]).json()]
    }
    threat_description_consider = {
        "Value": {
            "Properties": {
                "KeyValueOfstringstring": [
                    {
                        "Key": "UserThreatDescription",
                        "Value": "BEFORE. Consider AFTER."
                    }
                ]
            }
        }
    }
    threat_description_without_consider = {
        "Value": {
            "Properties": {
                "KeyValueOfstringstring": [
                    {
                        "Key": "UserThreatDescription",
                        "Value": "No consider pattern."
                    }
                ]
            }
        }
    }
    threat_short_description_consider = {
        "Value": {
            "Properties": {
                "KeyValueOfstringstring": [
                    {
                        "Key": "UserThreatShortDescription",
                        "Value": "BEFORE. Consider AFTER."
                    }
                ]
            }
        }
    }
    threat_short_description_without_consider = {
        "Value": {
            "Properties": {
                "KeyValueOfstringstring": [
                    {
                        "Key": "UserThreatShortDescription",
                        "Value": "No consider pattern."
                    }
                ]
            }
        }
    }
    threat_without_description = {
        "Value": {
            "Properties": {
                "KeyValueOfstringstring": [
                    {
                        "Key": "NoRealKey",
                        "Value": "This value belongs to a non real key from MTMT files. No description."
                    }
                ]
            }
        }
    }
    threat_with_mitigation = {
        "Value": {
            "Properties": {
                "KeyValueOfstringstring": [
                    {
                        "Key": "UserThreatDescription",
                        "Value": "Threat Description. Consider Mitigation Name. Mitigation Description."
                    }
                ]
            }
        }
    }
    threat_without_mitigation = {
        "Value": {
            "Properties": {
                "KeyValueOfstringstring": [
                    {
                        "Key": "UserThreatDescription",
                        "Value": "Threat Description."
                    }
                ]
            }
        }
    }
    threat_with_mitigation_short_description = {
        "Value": {
            "Properties": {
                "KeyValueOfstringstring": [
                    {
                        "Key": "UserThreatShortDescription",
                        "Value": "Threat short description. Consider Mitigation Name. Mitigation Description."
                    }
                ]
            }
        }
    }
    threat_with_mitigation_no_description = {
        "Value": {
            "Properties": {
                "KeyValueOfstringstring": [
                    {
                        "Key": "NoRealKey",
                        "Value": "This value belongs to a non real key from MTMT files. No description."
                    }
                ]
            }
        }
    }

    def test_parse_mtmt(self):
        parser = MTMThreatParser(MTMT([], [], [MTMThreat(self.threat)], MTMKnowledge({})))
        threats, mitigations = parser.parse(self.components)

        assert threats[0].json() == self.expected_otm_threat
        assert mitigations[0].json() == self.expected_otm_mitigation
        assert self.components[0].json() == self.expected_component

    @pytest.mark.parametrize("mtmt_threat, expected_mitigation", [
        (MTMThreat(threat_azure), expected_otm_mitigation_azure),
        (MTMThreat(threat_azure_without_steps), expected_otm_mitigation_azure_without_steps),
    ])
    def test_parse_mtmt_azure(self, mtmt_threat, expected_mitigation):
        components = [
            Component(
                component_id="ff5f3e59-caa6-464c-8b3e-528d6a3dbfbb",
                name="Micro-Batch (Managed App)",
                component_type="web-application-server-side",
                parent="2ab4effa-40b7-4cd2-ba81-8247d29a6f2d",
                parent_type="trustZone",
                attributes={
                    "Name": "Micro-Batch (Managed App)",
                    "Out Of Scope": "false",
                    "Isolation Level": "Not Selected",
                    "Show Generic Process Threat": "Yes"
                }
            )
        ]
        parser = MTMThreatParser(MTMT([], [], [mtmt_threat], MTMKnowledge({})))
        threats, mitigations = parser.parse(components)

        assert threats[0].json() == self.expected_otm_threat_azure
        assert mitigations[0].json() == expected_mitigation
        assert components[0].json() == self.expected_component

    @pytest.mark.parametrize("mtmt_threat, expected_description", [
        (MTMThreat(threat_description_consider), "BEFORE"),
        (MTMThreat(threat_description_without_consider), "No consider pattern"),
        (MTMThreat(threat_short_description_consider), "BEFORE"),
        (MTMThreat(threat_short_description_without_consider), "No consider pattern"),
        (MTMThreat(threat_without_description), None)
    ])
    def test_get_threat_description(self, mtmt_threat, expected_description):
        description = get_threat_description(mtmt_threat)

        assert description == expected_description

    @pytest.mark.parametrize("mtmt_threat, expected_description", [
        (MTMThreat(threat_with_mitigation), "Consider Mitigation Name. Mitigation Description"),
        (MTMThreat(threat_without_mitigation), None),
        (MTMThreat(threat_with_mitigation_short_description), "Consider Mitigation Name. Mitigation Description"),
        (MTMThreat(threat_with_mitigation_no_description), None)
    ])
    def test_get_mitigation_description(self, mtmt_threat, expected_description):
        description = get_mitigation_description(mtmt_threat)

        assert description == expected_description

    @pytest.mark.parametrize("message, expected_message", [
        ("Mitigation Description Dot.", "Mitigation Description Dot"),
        ("Mitigation Description No Dot", "Mitigation Description No Dot"),
        ("Mitigation Description Dot. Mitigation Description Dot.", "Mitigation Description Dot. Mitigation Description Dot"),
        (None, None)
    ])
    def test_remove_trailing_dot(self, message, expected_message):
        message_without_trailing_dot = remove_trailing_dot(message)

        assert message_without_trailing_dot == expected_message

    def test_long_description(self):
        threat = MTMThreat({
            "Value": {
                "Properties": {
                    "KeyValueOfstringstring": [
                        {
                            "Key": "UserThreatDescription",
                            "Value": "This is a long description. Consider this."
                        }
                    ]
                }
            }
        })
        result = get_threat_description(threat)
        assert result == "This is a long description"

    def test_short_description(self):
        threat = MTMThreat({
            "Value": {
                "Properties": {
                    "KeyValueOfstringstring": [
                        {
                            "Key": "UserThreatShortDescription",
                            "Value": "No Short description. Consider that."
                        }
                    ]
                }
            }
        })
        result = get_threat_description(threat)
        assert result == "No Short description"

    def test_no_description(self):
        threat = MTMThreat({
            "Value": {
                "Properties": {
                    "KeyValueOfstringstring": [
                        {
                            "Key": "NonRealKey",
                            "Value": "This is a value for a non real key."
                        }
                    ]
                }
            }
        })
        result = get_threat_description(threat)
        assert result is None
