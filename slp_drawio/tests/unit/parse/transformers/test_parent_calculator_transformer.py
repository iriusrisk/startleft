from slp_drawio.slp_drawio.objects.diagram_objects import Diagram, DiagramComponent, DiagramTrustZone
from slp_drawio.slp_drawio.parse.tranformers.parent_calculator_transformer import ParentCalculatorTransformer


class TestParentCalculatorTransformer:

    def test_transform_with_parent_set(self):
        # GIVEN the trust zones
        tz1 = DiagramTrustZone('tz1', 'trustzone1', None)
        # AND the components
        c1 = DiagramComponent(id='c1', name='component1')
        c21 = DiagramComponent(id='c2.1', name='component2.1', shape_parent_id='c1')
        c22 = DiagramComponent(id='c2.2', name='component2.2', shape_parent_id='c1')
        c31 = DiagramComponent(id='c3.1', name='component3.1', shape_parent_id='c2.1')
        c32 = DiagramComponent(id='c3.2', name='component3.2', shape_parent_id='c2.1')
        c33 = DiagramComponent(id='c3.3', name='component3.3', shape_parent_id='c2.2')
        c41 = DiagramComponent(id='c4.1', name='component4.1', shape_parent_id='c3.3')
        # AND the Diagram
        diagram: Diagram = Diagram(components=[c1, c21, c22, c31, c32, c33, c41], default_trustzone=tz1)
        # AND the ParentCalculator transformer
        transformer = ParentCalculatorTransformer(diagram)

        # WHEN we transform the diagram
        transformer.transform()

        # THEN the diagram elements have the excepted parents
        assert len(diagram.components) == 7
        assert len(diagram.trustzones) == 0
        assert diagram.components[0].otm.json() == {'id': 'c1', 'name': 'component1', 'parent': {'None': None},
                                                    'type': None}
        assert diagram.components[1].otm.json() == {'id': 'c2.1', 'name': 'component2.1', 'parent': {'component': 'c1'},
                                                    'type': None}
        assert diagram.components[2].otm.json() == {'id': 'c2.2', 'name': 'component2.2', 'parent': {'component': 'c1'},
                                                    'type': None}
        assert diagram.components[3].otm.json() == {'id': 'c3.1', 'name': 'component3.1',
                                                    'parent': {'component': 'c2.1'},
                                                    'type': None}
        assert diagram.components[4].otm.json() == {'id': 'c3.2', 'name': 'component3.2',
                                                    'parent': {'component': 'c2.1'},
                                                    'type': None}
        assert diagram.components[5].otm.json() == {'id': 'c3.3', 'name': 'component3.3',
                                                    'parent': {'component': 'c2.2'},
                                                    'type': None}
        assert diagram.components[6].otm.json() == {'id': 'c4.1', 'name': 'component4.1',
                                                    'parent': {'component': 'c3.3'},
                                                    'type': None}
