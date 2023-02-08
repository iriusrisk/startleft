from otm.otm.entity.component import OtmComponent
from otm.otm.entity.dataflow import OtmDataflow
from otm.otm.entity.otm import Otm
from otm.otm.otm_pruner import OtmPruner
from otm.otm.provider import Provider


class DummyProvider(str, Provider):
    DUMMY = ("DUMMY", "Dummy", "diagram")


class TestIterationUtils:

    def test_prune_orphan_dataflows_with_no_orphan(self):
        # Given an otm with no orphan dataflows
        otm: Otm = Otm('test', 'test', DummyProvider.DUMMY)
        otm.dataflows = [OtmDataflow('from-1001-to-2002', None, '1001', '2002')]
        otm.components = [
            OtmComponent('1001', '', '', '', ''),
            OtmComponent('2002', '', '', '', '')
        ]

        # when we call prune_orphan_dataflows
        OtmPruner(otm).prune_orphan_dataflows()

        # we have the expected dataflows and components
        assert len(otm.dataflows) == 1
        assert len(otm.components) == 2

    def test_prune_orphan_dataflows_with_orphans(self):
        # Given an otm with orphan dataflows
        otm: Otm = Otm('test', 'test', DummyProvider.DUMMY)
        otm.dataflows = [
            OtmDataflow('from-1001-to-2002', None, '1001', '2002'),
            OtmDataflow('from-2001-to-1001', None, '2002', '1001'),
            OtmDataflow('from-AAA-to-1001', None, 'AAA', '1001'),
            OtmDataflow('from-1001-to-BBB', None, '1001', 'BBB'),
            OtmDataflow('from-AAA-to-BBB', None, 'AAA', 'BBB'),
            OtmDataflow('from-3003-to-ZZZ', None, '3003', 'ZZZ')
        ]
        otm.components = [
            OtmComponent('1001', '', '', '', ''),
            OtmComponent('2002', '', '', '', ''),
            OtmComponent('3003', '', '', '', ''),
            OtmComponent('ZZZ', '', '', '', ''),
            OtmComponent('999', '', '', '', '')
        ]

        # when we call prune_orphan_dataflows
        OtmPruner(otm).prune_orphan_dataflows()

        # we have the expected dataflows and components
        assert len(otm.dataflows) == 3
        assert len(otm.components) == 5
