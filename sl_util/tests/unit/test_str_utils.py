from pytest import mark

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

    @mark.parametrize('source', [0, '0', 'zero'])
    def test_number_conversions_to_zero(self, source):
        # Given the source
        # when passed 0 to function
        number1 = to_number(source)
        # when passed '0' to function
        number2 = to_number(source)
        # when passed 'zero' to function
        number3 = to_number(source)
        # Then we obtain 0
        assert number1 == number2 == number3 == 0

    @mark.parametrize('source', [1, '1', 'one'])
    def test_number_conversions_to_one(self, source):
        # Given the source
        # when passed 1 to function
        number1 = to_number(source)
        # when passed '1' to function
        number2 = to_number(source)
        # when passed 'one' to function
        number3 = to_number(source)
        # Then we obtain 1
        assert number1 == number2 == number3 == 1

    @mark.parametrize('source', [2, '2', 'two'])
    def test_number_conversions_to_two(self, source):
        # Given the source
        # when passed 2 to function
        number1 = to_number(source)
        # when passed '2' to function
        number2 = to_number(source)
        # when passed 'two' to function
        number3 = to_number(source)
        # Then we obtain 2
        assert number1 == number2 == number3 == 2

    @mark.parametrize('source', ['sandbox', ''])
    def test_number_conversions_to_alphanumeric(self, source):
        # Given the source
        # when passed an alphanumeric to function
        number1 = to_number(source)
        # when passed an empty string to function
        number2 = to_number(source)
        # Then we obtain default value 0
        assert number1 == number2 == 0
