from otm.otm.entity.parent_type import ParentType
from slp_drawio.slp_drawio.objects.diagram_objects import Diagram, DiagramComponent, DiagramTrustZone, DiagramDataflow
from slp_drawio.slp_drawio.parse.transformers.parent_calculator_transformer import ParentCalculatorTransformer, \
    get_parent_type


class TestParentCalculatorTransformer:

    def test_transform_with_parent_set(self):
        # GIVEN the trust zones
        tz0 = DiagramTrustZone('1a', id_='tz0', name='trustzone0', default=True)
        tz1 = DiagramTrustZone('2b', id_='tz1', name='trustzone1')
        tz2 = DiagramTrustZone('3c', id_='tz2', name='trustzone2', shape_parent_id='c2.1')
        tz3 = DiagramTrustZone('4d', id_='tz3', name='trustzone3', shape_parent_id='tz2')
        # AND the components
        c1 = DiagramComponent(id='c1', name='component1')
        c21 = DiagramComponent(id='c2.1', name='component2.1', shape_parent_id='tz1')
        c22 = DiagramComponent(id='c2.2', name='component2.2', shape_parent_id='tz1')
        c23 = DiagramComponent(id='c2.3', name='component2.3', shape_parent_id='tz1')
        c31 = DiagramComponent(id='c3.1', name='component3.1', shape_parent_id='tz3')
        c32 = DiagramComponent(id='c3.2', name='component3.2', shape_parent_id='tz3')
        c33 = DiagramComponent(id='c3.3', name='component3.3', shape_parent_id='tz3')
        c41 = DiagramComponent(id='c4.1', name='component4.1', shape_parent_id='c3.3')
        c42 = DiagramComponent(id='c4.2', name='component4.2', shape_parent_id='c3.3')
        # AND the Diagram
        diagram: Diagram = Diagram(
            components=[c1, c21, c22, c23, c31, c32, c33, c41, c42],
            trustzones=[tz1, tz2, tz3],
            default_trustzone=tz0)
        # AND the ParentCalculator transformer
        transformer = ParentCalculatorTransformer(diagram)

        # WHEN we transform the diagram
        transformer.transform()

        # THEN the diagram elements have the excepted parents
        assert len(diagram.components) == 9
        assert len(diagram.trustzones) == 3
        assert diagram.components[0].otm.json() == {'id': 'c1', 'name': 'component1', 'parent': {'None': None},
                                                    'type': None}
        assert diagram.components[1].otm.json() == {'id': 'c2.1', 'name': 'component2.1',
                                                    'parent': {'trustZone': 'tz1'},
                                                    'type': None}
        assert diagram.components[2].otm.json() == {'id': 'c2.2', 'name': 'component2.2',
                                                    'parent': {'trustZone': 'tz1'},
                                                    'type': None}
        assert diagram.components[3].otm.json() == {'id': 'c2.3', 'name': 'component2.3',
                                                    'parent': {'trustZone': 'tz1'},
                                                    'type': None}
        assert diagram.components[4].otm.json() == {'id': 'c3.1', 'name': 'component3.1',
                                                    'parent': {'trustZone': 'tz3'},
                                                    'type': None}
        assert diagram.components[5].otm.json() == {'id': 'c3.2', 'name': 'component3.2',
                                                    'parent': {'trustZone': 'tz3'},
                                                    'type': None}
        assert diagram.components[6].otm.json() == {'id': 'c3.3', 'name': 'component3.3',
                                                    'parent': {'trustZone': 'tz3'},
                                                    'type': None}
        assert diagram.components[7].otm.json() == {'id': 'c4.1', 'name': 'component4.1',
                                                    'parent': {'component': 'c3.3'},
                                                    'type': None}
        assert diagram.components[8].otm.json() == {'id': 'c4.2', 'name': 'component4.2',
                                                    'parent': {'component': 'c3.3'},
                                                    'type': None}
        assert diagram.trustzones[0].otm.json() == {'id': 'tz1', 'name': 'trustzone1', 'risk': {'trustRating': 10},
                                                    'type': '2b'}
        assert diagram.trustzones[1].otm.json() == {'id': 'tz2', 'name': 'trustzone2', 'parent': {'component': 'c2.1'},
                                                    'risk': {'trustRating': 10}, 'type': '3c'}
        assert diagram.trustzones[2].otm.json() == {'id': 'tz3', 'name': 'trustzone3', 'parent': {'trustZone': 'tz2'},
                                                    'risk': {'trustRating': 10}, 'type': '4d'}

    def test_get_parent_type(self):
        assert get_parent_type(DiagramTrustZone('8a')) == ParentType.TRUST_ZONE
        assert get_parent_type(DiagramComponent('99')) == ParentType.COMPONENT
        assert get_parent_type(DiagramDataflow('zz')) is None
