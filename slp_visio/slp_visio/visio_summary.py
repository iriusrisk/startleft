import logging
import os
from typing import List

from otm.otm.entity.otm import OTM
from slp_base import DiagramType
from slp_visio import VisioProcessor
from slp_visio.slp_visio.util.visio import normalize_label

logger = logging.getLogger(__name__)


def _find_otm_component_by_id(otm: OTM, _id: str):
    if not otm or not otm.components:
        return
    for c in otm.components:
        if c.id == _id:
            return c


def _find_otm_tz_by_id(otm: OTM, _id: str):
    if not otm or not otm.trustzones:
        return
    for tz in otm.trustzones:
        if tz.id == _id:
            return tz


def _get_visio_components(processor: VisioProcessor):
    """
    Returns the components array available at the given source file
    It is needed to reload the provider because the otm process modifies this components array
    :param processor: The visio processor
    :return: A visio shape arrays
    """
    loader = processor.get_provider_loader()
    loader.load()
    return loader.get_visio().components


class VisioSummary:

    def __init__(
            self, source_files: List, mappings: [bytes], diag_type: DiagramType = None):
        self.__source_files = source_files
        self.__mappings = mappings
        self.__diag_type = diag_type

    def __exists_mappings(self):
        return self.__mappings and len(self.__mappings) > 0

    def get_elements(self) -> List[dict]:
        elements: List[dict] = []
        for _file in self.__source_files:
            file_name = os.path.basename(_file.name)
            try:
                processor = VisioProcessor('id', 'name', _file, self.__mappings, diag_type=self.__diag_type)
                otm = None
                if self.__exists_mappings():
                    otm = processor.process()
                for c in _get_visio_components(processor):
                    element = {'SOURCE': file_name, 'SOURCE_ELEMENT_TYPE': normalize_label(c.type),
                               'SOURCE_ELEMENT_NAME': c.name}
                    if self.__exists_mappings():
                        otm_c = _find_otm_component_by_id(otm, c.id)
                        otm_z = _find_otm_tz_by_id(otm, c.id)
                        element['OTM_MAPPED_TYPE'] = otm_c.type if otm_c else \
                            f'Trustzone[{otm_z.name}]' if otm_z else ''
                    elements.append(element)
            except Exception as e:
                logger.error(f'It has been an error when summary the {file_name} file. Error info: {e}')
                raise e

        return elements
