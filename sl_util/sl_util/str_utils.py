import random
import uuid


def deterministic_uuid(source):
    if source:
        random.seed(source)
    return str(uuid.UUID(int=random.getrandbits(128), version=4))
