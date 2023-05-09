import random
import uuid


def deterministic_uuid(source):
    if source:
        random.seed(source)
    return str(uuid.UUID(int=random.getrandbits(128), version=4))


def get_bytes(s: str, encoding='utf-8') -> bytes:
    return bytes(s, encoding)
