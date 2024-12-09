import random
import uuid
from word2number import w2n


def deterministic_uuid(source):
    if source:
        random.seed(source)
    return str(uuid.UUID(int=random.getrandbits(128), version=4))


def get_bytes(s: str, encoding='utf-8') -> bytes:
    return bytes(s, encoding)


def to_number(input, default_value: int = 0) -> int:
    try:
        return int(input)
    except ValueError:
        try:
            return w2n.word_to_num(input)
        except ValueError:
            return default_value

def truncate(s: str, max_length: int) -> str:
    return s[:max_length] if s else s