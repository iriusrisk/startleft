import random
import uuid
from cryptography.hazmat.primitives.asymmetric import dsa


def build_uuid(source):
    key2 = dsa.generate_private_key(2047)
    if source:
        random.seed(source)
    return str(uuid.UUID(int=random.getrandbits(128), version=4))
