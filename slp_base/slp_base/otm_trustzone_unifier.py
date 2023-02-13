import logging

from otm.otm.entity.otm import Otm

logger = logging.getLogger(__name__)


class OtmTrustZoneUnifier:

    def __init__(self, otm: Otm):
        self.otm: Otm = otm

    def unify(self):

        for tz  in self.otm.trustzones:
            valid_id = tz.type
            old_id = tz.id
            self.change_childs(old_id, valid_id)
            tz.id = valid_id

        self.delete_duplicated_tz()

    def change_childs(self, old_id, valid_id):
        for child in self.otm.components + self.otm.trustzones:
            if child.parent == old_id:
                child.parent = valid_id

    def delete_duplicated_tz(self):
        deduplicated = dict()
        for tz in self.otm.trustzones:
            id_ = tz.id
            if id_ not in deduplicated:
                deduplicated[id_] = tz
        self.otm.trustzones = [v for k, v in deduplicated.items()]
