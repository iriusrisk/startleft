from slp_base import DiagramType
from slp_visio.slp_visio.load.objects.diagram_objects import Diagram, DiagramComponent, DiagramConnector
from slp_visio.slp_visio.parse.diagram_pruner import DiagramPruner


class TestDiagramPruner:

    def test_no_mapping_labels(self):
        # GIVEN a list of components
        components = [DiagramComponent('1', 'Component 1'), DiagramComponent('2', 'Component 2')]

        # AND no connectors
        connectors = []

        # AND no mapping labels
        mapping_labels = []

        # WHEN calling run
        diagram = Diagram(DiagramType.VISIO, components, connectors)
        DiagramPruner(diagram, mapping_labels).run()

        # THEN all components and connectors are pruned
        assert len(diagram.components) == 0
        assert len(diagram.connectors) == 0

    def test_simple_unrelated_elements(self):
        # GIVEN a list of no nested components
        components = [DiagramComponent('1', 'Component 1'), DiagramComponent('2', 'Component 2')]

        # AND no connectors
        connectors = []

        # AND mapping labels matching all given components
        mapping_labels = ['Component-1', 'Component-2']

        # WHEN calling run
        diagram = Diagram(DiagramType.VISIO, components, connectors)
        DiagramPruner(diagram, mapping_labels).run()

        # THEN diagram is left as is
        assert len(diagram.components) == 2
        assert len(diagram.connectors) == 0

    def test_simple_connected_elements(self):
        # GIVEN two no nested components
        components = [DiagramComponent('1', 'Component 1'), DiagramComponent('2', 'Component 2')]

        # AND a connector between them
        connectors = [DiagramConnector('12', '1', '2')]

        # AND mapping labels matching all given components
        mapping_labels = ['Component-1', 'Component-2']

        # WHEN calling run
        diagram = Diagram(DiagramType.VISIO, components, connectors)
        DiagramPruner(diagram, mapping_labels).run()

        # THEN diagram is left as is
        assert len(diagram.components) == 2
        assert len(diagram.connectors) == 1

    def test_simple_connected_elements_only_one_mapped(self):
        # GIVEN two no nested components
        components = [DiagramComponent('1', 'Component 1'), DiagramComponent('2', 'Component 2')]

        # AND a connector between them
        connectors = [DiagramConnector('12', '1', '2')]

        # AND mapping labels with only one component mapped
        mapping_labels = ['Component-1']

        # WHEN calling run
        diagram = Diagram(DiagramType.VISIO, components, connectors)
        DiagramPruner(diagram, mapping_labels).run()

        # THEN the non mapped component and the connector are removed
        assert len(diagram.components) == 1
        assert len(diagram.connectors) == 0

    def test_nested_unrelated_elements(self):
        # GIVEN a set of nested components
        trustzone = DiagramComponent(id='TZ1', name='Trustzone 1')

        grandparent = DiagramComponent(id='GP1', name='Grandparent 1', parent=trustzone)
        parent = DiagramComponent(id='P1', name='Parent 1', parent=grandparent)
        grandchild = DiagramComponent(id='GC1', name='Grandchild 1', parent=parent)

        child = DiagramComponent(id='C1', name='Child 1', parent=trustzone)

        components = [
            trustzone,
            grandparent,
            parent,
            grandchild,
            child
        ]

        # AND no connectors
        connectors = []

        # AND mapping labels that does not map an intermediate component
        mapping_labels = [
            # 'Trustzone 1',
            'Grandparent-1',
            # 'Parent 1',
            'Grandchild-1',
            'Child-1'
        ]

        # WHEN calling run
        diagram = Diagram(DiagramType.VISIO, components, connectors)
        DiagramPruner(diagram, mapping_labels).run()

        # THEN the non mapped components are removed
        assert len(diagram.components) == 3

        # AND the parents are recalculated
        assert not grandparent.parent
        assert not child.parent
        assert grandchild.parent.id == 'GP1'

    def test_nested_connected_elements(self):
        # GIVEN a set of nested components
        trustzone = DiagramComponent(id='TZ1', name='Trustzone 1')

        grandparent = DiagramComponent(id='GP1', name='Grandparent 1', parent=trustzone)
        parent = DiagramComponent(id='P1', name='Parent 1', parent=grandparent)
        grandchild = DiagramComponent(id='GC1', name='Grandchild 1', parent=parent)

        child = DiagramComponent(id='C1', name='Child 1', parent=trustzone)
        child2 = DiagramComponent(id='C2', name='Child 2', parent=trustzone)

        components = [
            trustzone,
            grandparent,
            parent,
            grandchild,
            child,
            child2
        ]

        # AND connectors between mapped and non mapped elements
        connectors = [
            DiagramConnector('P1C1', 'P1', 'C1'),
            DiagramConnector('P1C2', 'P1', 'C2'),
            DiagramConnector('C1GC1', 'C1', 'GC1'),
        ]

        # AND mapping labels that does not map an intermediate component
        mapping_labels = [
            # 'Trustzone 1',
            'Grandparent-1',
            # 'Parent 1',
            'Grandchild-1',
            'Child-1'
        ]

        # WHEN calling run
        diagram = Diagram(DiagramType.VISIO, components, connectors)
        DiagramPruner(diagram, mapping_labels).run()

        # THEN the non mapped components are removed
        assert len(diagram.components) == 3

        # AND the parents are recalculated
        assert not grandparent.parent
        assert not child.parent
        assert grandchild.parent.id == 'GP1'

        # AND orphan connector is prunned
        assert len(diagram.connectors) == 1
        assert diagram.connectors[0].id == 'C1GC1'
