from pytest import mark
from random import randint
from unittest.mock import patch
from sl_util.sl_util.str_utils import deterministic_uuid, to_number


class TestStrUtils:

    @mark.parametrize('source,expected', [
        ('public-cloud', '69eff760-1b3c-49f9-9b8b-924ed4a83bf5'),
        ('private-cloud', '9a5b8012-1802-4752-bc80-2699c6fffb77'),
        ('internet', '0d56245c-c930-4d32-ae42-e4be5ead51d5'),
        (' ', '52d07498-8a4f-46de-84a1-3527363060fa'),
        ('  ', '5ceae64c-acb0-4c57-91dc-643071b0291c')
    ])
    def test_deterministic_uuid(self, source, expected):
        # Given the source
        # when passed to function
        uuid = deterministic_uuid(source)
        # Then we obtain the expected uuid
        assert uuid == expected

    @mark.parametrize('source', [None, ''])
    def test_deterministic_uuid_without_source(self, source):
        # Given the source
        # when obtainan a first uuid
        uuid1 = deterministic_uuid(source)
        # when obtainan a second uuid
        uuid2 = deterministic_uuid(source)
        # Then we obtain two different values
        assert uuid1 != uuid2

    @mark.parametrize('source', [randint(0, 100), str(randint(0, 100))])
    def test_to_number(self, source):
        # GIVEN a random integer

        # WHEN it is transformed to a number
        result = to_number(source)

        # THEN we obtain the original number
        assert result == int(source)

    @patch('sl_util.sl_util.str_utils.w2n.word_to_num', return_value=2)
    def test_text_to_number(self, mocked_word_to_otm):
        # GIVEN a text number
        source = 'two'

        # WHEN it is transformed to a number
        result = to_number(source)

        # THEN we obtain the number
        assert result == 2

    def test_unknown_to_number(self):
        # GIVEN an unkown
        source = 'unknown'

        # AND a default value
        default_value = 5

        # WHEN it is transformed to a number
        result = to_number(source, default_value)

        # THEN we obtain the default value
        assert result == 5

    @mark.parametrize('source', ['sandbox', ''])
    def test_number_conversions_to_alphanumeric(self, source):
        # Given the source
        # when passed an alphanumeric to function
        number1 = to_number(source)
        # when passed an empty string to function
        number2 = to_number(source)
        # Then we obtain default value 0
        assert number1 == number2 == 0
