import logging

from otm.otm.entity.otm import OTM

logger = logging.getLogger(__name__)

PERMIT_ANY_REPRESENTATIONS_VOID = False


class OTMRepresentationsPruner:

    def __init__(self, otm: OTM):
        self.otm: OTM = otm

    def prune(self):
        if PERMIT_ANY_REPRESENTATIONS_VOID:
            return

        any_representation_empty = self.is_any_representation_empty()

        if any_representation_empty:
            self.remove_all_representations()

    def is_any_representation_empty(self):

        if not self.otm.representations:
            return True

        for trustzone in self.otm.trustzones:
            if not trustzone.representations:
                return True

        for component in self.otm.components:
            if not component.representations:
                return True

        return False

    def remove_all_representations(self):
        for trustzone in self.otm.trustzones:
            trustzone.representations = None

        for component in self.otm.components:
            component.representations = None
