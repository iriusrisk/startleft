from otm.otm.entity.component import Component
from otm.otm.entity.dataflow import Dataflow
from otm.otm.entity.otm import OTM
from otm.otm.entity.representation import RepresentationType
from otm.otm.otm_pruner import OTMPruner
from otm.otm.provider import Provider


class DummyProvider(str, Provider):
    DUMMY = ("DUMMY", "Dummy", RepresentationType.DIAGRAM)


class TestIterationUtils:

    def test_prune_orphan_dataflows_with_no_orphan(self):
        # Given an otm with no orphan dataflows
        otm: OTM = OTM('test', 'test', DummyProvider.DUMMY)
        otm.dataflows = [Dataflow('from-1001-to-2002', None, '1001', '2002')]
        otm.components = [
            Component('1001', '', '', '', ''),
            Component('2002', '', '', '', '')
        ]

        # when we call prune_orphan_dataflows
        OTMPruner(otm).prune_orphan_dataflows()

        # we have the expected dataflows and components
        assert len(otm.dataflows) == 1
        assert len(otm.components) == 2

    def test_prune_orphan_dataflows_with_orphans(self):
        # Given an otm with orphan dataflows
        otm: OTM = OTM('test', 'test', DummyProvider.DUMMY)
        otm.dataflows = [
            Dataflow('from-1001-to-2002', None, '1001', '2002'),
            Dataflow('from-2001-to-1001', None, '2002', '1001'),
            Dataflow('from-AAA-to-1001', None, 'AAA', '1001'),
            Dataflow('from-1001-to-BBB', None, '1001', 'BBB'),
            Dataflow('from-AAA-to-BBB', None, 'AAA', 'BBB'),
            Dataflow('from-3003-to-ZZZ', None, '3003', 'ZZZ')
        ]
        otm.components = [
            Component('1001', '', '', '', ''),
            Component('2002', '', '', '', ''),
            Component('3003', '', '', '', ''),
            Component('ZZZ', '', '', '', ''),
            Component('999', '', '', '', '')
        ]

        # when we call prune_orphan_dataflows
        OTMPruner(otm).prune_orphan_dataflows()

        # we have the expected dataflows and components
        assert len(otm.dataflows) == 3
        assert len(otm.components) == 5

    def test_prune_self_reference_dataflows(self):
        # GIVEN an otm with some self reference dataflows
        otm: OTM = OTM('test', 'test', DummyProvider.DUMMY)
        otm.dataflows = [
            Dataflow('A', None, '1001', '2002'),
            Dataflow('B', None, '2002', '2002'),
            Dataflow('C', None, '2002', '1001')
        ]

        # WHEN we call prune_self_reference_dataflows
        OTMPruner(otm).prune_self_reference_dataflows()

        # THEN we have the expected dataflows
        assert len(otm.dataflows) == 2
        assert otm.dataflows[0].id == 'A'
        assert otm.dataflows[1].id == 'C'


