from slp_mtmt.slp_mtmt.entity.mtmt_entity_threatinstance import MTMThreat


class TestMTMThreat:
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
                        "Value": "An adversary may gain unauthorized access to Azure Data Factory (ingest) account in a subscription"
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

    def test_mtmt_threat_fields(self):
        mtmt_threat = MTMThreat(self.threat)

        assert mtmt_threat.dataflow_id == "501a8a2a-19ad-49f1-8ff8-0740bc303214"
        assert mtmt_threat.source_component_id == "8668f6af-f5a0-47eb-ad27-ce8a7d16303b"
        assert mtmt_threat.destination_component_id == "ff5f3e59-caa6-464c-8b3e-528d6a3dbfbb"
        assert mtmt_threat.id == 30
        assert mtmt_threat.threat_priority == "High"
        assert mtmt_threat.threat_state == "Mitigated"
        assert mtmt_threat.justification is None
        assert mtmt_threat.title == "Web Application Process Memory Tampered"
        assert mtmt_threat.threat_category == "Tampering"
        assert mtmt_threat.short_description == "Tampering is the act of altering the bits. Tampering with a process involves changing bits in the running process."
        assert mtmt_threat.long_description == "If Web Application is given access to memory, such as shared memory or pointers, or is given the ability to control what Web Service executes (for example, passing back a function pointer.), then Web Application can tamper with Web Service. Consider if the function could work with less access to memory, such as passing data rather than pointers."
        assert mtmt_threat.possible_mitigations is None
        assert mtmt_threat.steps is None
        assert mtmt_threat.mitigation_effort is None
        assert mtmt_threat.from_azure_template is False

    def test_mtmt_threat_azure_fields(self):
        mtmt_threat = MTMThreat(self.threat_azure)

        assert mtmt_threat.dataflow_id == "501a8a2a-19ad-49f1-8ff8-0740bc303214"
        assert mtmt_threat.source_component_id == "8668f6af-f5a0-47eb-ad27-ce8a7d16303b"
        assert mtmt_threat.destination_component_id == "ff5f3e59-caa6-464c-8b3e-528d6a3dbfbb"
        assert mtmt_threat.id == 30
        assert mtmt_threat.threat_priority == "High"
        assert mtmt_threat.threat_state == "Mitigated"
        assert mtmt_threat.justification is None
        assert mtmt_threat.title == "An adversary may gain unauthorized access to Azure Data Factory (ingest) account in a subscription"
        assert mtmt_threat.threat_category == "Elevation Of Privilege"
        assert mtmt_threat.short_description == "A user subject gains increased capability or privilege by taking advantage of an implementation bug."
        assert mtmt_threat.long_description == "An adversary may gain unauthorized access to Azure Data Factory (ingest) account in a subscription"
        assert mtmt_threat.possible_mitigations == 'Enable Role-Based Access Control (RBAC) to Azure storage account using Azure Resource Manager. Refer: &lt;a href="https://aka.ms/tmtauthz#rbac-azure-manager"&gt;https://aka.ms/tmtauthz#rbac-azure-manager&lt;/a&gt;'
        assert mtmt_threat.steps == "When you create a new storage account, you select a deployment model of Classic or Azure Resource Manager. The Classic model of creating resources in Azure only allows all-or-nothing access to the subscription, and in turn, the storage account. With the Azure Resource Manager model, you put the storage account in a resource group and control access to the management plane of that specific storage account using Azure Active Directory. For example, you can give specific users the ability to access the storage account keys, while other users can view information about the storage account, but cannot access the storage account keys."
        assert mtmt_threat.mitigation_effort == "Low"
        assert mtmt_threat.from_azure_template is True
