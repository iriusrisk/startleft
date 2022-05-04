from vsdx import VisioFile

from startleft.otm import OTM
from startleft.diagram.otm_builder import OtmBuilder
from startleft.diagram.page_to_diagram import PageToDiagram


class VisioToOtm:
    visio_filename: str

    def __init__(self, visio_filename: str):
        self.visio_filename = visio_filename

    def run(self) -> OTM:
        with VisioFile(self.visio_filename) as vis:
            diagram_main_page = vis.pages[0].shapes[0]

            visio_diagram = PageToDiagram(diagram_main_page).run()

            return OtmBuilder(visio_diagram).build()
