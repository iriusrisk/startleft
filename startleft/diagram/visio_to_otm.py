from vsdx import VisioFile

from startleft.otm import OTM
from startleft.diagram.otm_builder import OtmBuilder
from startleft.diagram.page_to_diagram import PageToDiagram


class VisioToOtm:
    def __init__(self, visio_filename: str):
        self.visio_filename = visio_filename

    def run(self, mapping_file, project_name: str, project_id: str) -> OTM:
        with VisioFile(self.visio_filename) as vis:
            diagram_main_page = vis.pages[0].shapes[0]

            visio_diagram = PageToDiagram(diagram_main_page).run()

            return OtmBuilder(visio_diagram, mapping_file).build(project_name, project_id)
