from pytest import mark

from sl_util.sl_util.str_utils import deterministic_uuid


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
