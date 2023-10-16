from tempfile import SpooledTemporaryFile


class DrawIOToDict:

    def __init__(self, source):
        file: SpooledTemporaryFile = source.file
        content: bytes = file.read()
        self.source = content.decode()

    def to_dict(self) -> dict:
        return {}
