from slp_visio.slp_visio.validate.visio_validator import VisioValidator, VALID_MIME as VISIO_VALID_MIME


VALID_MIME = VISIO_VALID_MIME.copy()
VALID_MIME.append('application/zip')


class LucidValidator(VisioValidator):

    def __init__(self, file):
        super().__init__(file, VALID_MIME)
