from slp_visio.slp_visio.parse.visio_parser import VisioParser


class LucidParser(VisioParser):

    def build_otm(self):
        return super()._build_otm(self._map_trustzones(), self._map_components(), self._map_dataflows())
