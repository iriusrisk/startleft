import html
import random
import uuid

from word2number import w2n

from sl_util.sl_util import secure_regex as re


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


def remove_html_tags_and_entities(s: str) -> str:
    if s is None:
        return ''

    pattern_tags = re.compile(r'<\s*/?\s*[a-zA-Z]+.*?>')
    no_html = re.sub(pattern_tags, ' ', s).strip() if s else s

    pattern_spaces = re.compile(r'\s+')
    no_spaces = re.sub(pattern_spaces, ' ', no_html) if no_html else no_html

    return html.unescape(no_spaces).replace('\xa0', ' ').strip()
