from typing import Literal
from unittest.mock import MagicMock

import pytest

from otm.otm.entity.parent_type import ParentType
from slp_visio.slp_visio.parse.visio_parser import VisioParser

tz1 = MagicMock(id='tz1')
tz1.name = 'AWS Region: us-east-1'
tz1.type = 'RegionAWS2021'
tz1.parent = None

c1 = MagicMock(id='c1')
c1.name = 'EC2 instance'
c1.type = 'AmazonEC2instance2017'
c1.parent = tz1

c2 = MagicMock(id='c2')
c2.name = 'S3'
c2.type = 'AmazonS32017'
c2.parent = c1

c3 = MagicMock(id='c3')
c3.name = 'S3'
c3.type = 'AmazonSimpleStorageServiceS3AWS19'
c3.parent = None

c4 = MagicMock(id='c4')
c4.name = 'ignore'
c4.type = 'ignore'
c4.parent = None

diagram_components = [tz1, c1, c2, c3, c4]

default_trustzone = MagicMock(id='1', type='default-trustzone')


def get_default_trustzone():
    return default_trustzone


mapping_loader = MagicMock()
mapping_loader.get_default_otm_trustzone = get_default_trustzone

representation_calculator = MagicMock(calculate_representation=MagicMock())


def trustzone_mappings(mapping_type: Literal['label', 'list', 'regex']):
    def mappings():
        if mapping_type == 'label':
            return [{
                'id': 'id',
                'type': 'type',
                'label': 'Region'
            }]
        elif mapping_type == 'list':
            return [{
                'id': 'id',
                'type': 'type',
                'label': ['Region']
            }]
        else:
            return [{
                'id': 'id',
                'type': 'type',
                'label': {'$regex': '^AWS Region:.*$'}
            }]

    return mappings


def get_component_mappings(mapping_type: Literal['label', 'list', 'regex']):
    def mappings():
        if mapping_type == 'label':
            return [
                {'label': 'EC2 instance', 'type': 'ec2'},
                {'label': 'AmazonS32017', 'type': 's3'},
                {'label': 'AmazonSimpleStorageServiceS3', 'type': 's3'},
            ]
        elif mapping_type == 'list':
            return [
                {'label': ['AmazonEC2instance2017'], 'type': 'ec2'},
                {'label': ['S3'], 'type': 's3'}
            ]
        else:
            return [
                {'label': {'$regex': '^AmazonEC2.*$'}, 'type': 'ec2'},
                {'label': {'$regex': '^.*S3.*$'}, 'type': 's3'}
            ]

    return mappings


class TestVisioParser:

    @pytest.mark.parametrize('mapping_type', [
        pytest.param('label', id="by label"),
        pytest.param('list', id="by list"),
        pytest.param('regex', id="by regex")
    ])
    def test_build_otm_mapping_by_label(self, mapping_type):
        # GIVEN a mapping loader by mapping_type
        mapping_loader.get_trustzone_mappings = trustzone_mappings(mapping_type)
        mapping_loader.get_component_mappings = get_component_mappings(mapping_type)

        visio_parser = VisioParser(
            'project_id',
            'project_name',
            MagicMock(components=diagram_components),
            mapping_loader
        )
        visio_parser.representations = [MagicMock()]
        visio_parser._representation_calculator = MagicMock()

        # WHEN map_by_label is called
        otm = visio_parser.build_otm()

        # THEN the OTM is correctly generated
        # AND the components and trustzones are generated
        assert len(otm.trustzones) == 2
        assert otm.trustzones[0].id == tz1.id
        assert otm.trustzones[0].name == tz1.name
        assert otm.trustzones[1].id == default_trustzone.id
        assert otm.trustzones[1].name == default_trustzone.name

        assert len(otm.components) == 3
        assert otm.components[0].id == c1.id
        assert otm.components[0].name == c1.name
        assert otm.components[0].type == 'ec2'
        assert otm.components[0].parent == tz1.id
        assert otm.components[0].parent_type == ParentType.TRUST_ZONE

        assert otm.components[1].id == c2.id
        assert otm.components[1].name == c2.name
        assert otm.components[1].type == 's3'
        assert otm.components[1].parent == c1.id
        assert otm.components[1].parent_type == ParentType.COMPONENT

        assert otm.components[2].id == c3.id
        assert otm.components[2].name == c3.name
        assert otm.components[2].type == 's3'
        assert otm.components[2].parent == default_trustzone.id
        assert otm.components[2].parent_type == ParentType.TRUST_ZONE



