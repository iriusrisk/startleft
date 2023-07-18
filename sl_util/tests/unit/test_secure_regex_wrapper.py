from pytest import mark, param

import sl_util.sl_util.secure_regex  as sre


class TestSecureRegexWrapper:

    @mark.parametrize('expression, value, expected', [
        param('^a+$', 'a' * 999, 'a' * 999, id='duplicated_a'),
        param('^(a+)+$', 'a' * 999, 'a' * 999, id='duplicated_a_evil_regex'),

    ])
    def test_match(self, expression, value, expected):
        match = sre.match(expression, value)
        assert match.string == expected

    @mark.parametrize('expression, value', [
        param('^a+$', 'a' * 999 + 'X', id='duplicated_a'),
        param('^(a+)+$', 'a' * 999 + 'X', id='duplicated_a_evil_regex'),

    ])
    def test_no_match(self, expression, value):
        assert not sre.match(expression, value)

    @mark.parametrize('pattern, replace, string, expected', [
        param('^a+$', 'a', 'a' * 999, 'a', id='duplicated_a_match'),
        param('^a+$', 'a', 'a' * 999 + 'X', 'a' * 999 + 'X', id='duplicated_a_not_match'),
        param('^(a+)+$', 'a', 'a' * 999 + 'X', 'a' * 999 + 'X', id='evil_regex'),

    ])
    def test_sub(self, pattern, replace, string, expected):
        assert sre.sub(pattern, replace, string) == expected

    @mark.parametrize('text, expected', [
        param('\n\x0b', '\\\n\\\x0b', id='non_printable'),
    ])
    def test_escape(self, text, expected):
        assert sre.escape(text) == expected

    @mark.parametrize('expression, value, expected', [
        param('^a+$', 'a' * 999, ['a' * 999], id='duplicated_a'),
        param('a+', 'X' + 'a' * 999 + 'X' + 'a' * 999, ['a' * 999, 'a' * 999], id='duplicated_a_2_times'),
        param('^(a+)+$', 'a' * 999, ['a' * 999], id='duplicated_a_evil_regex'),

    ])
    def test_find_all(self, expression, value, expected):
        assert sre.findall(expression, value) == expected

    @mark.parametrize('expression, value, expected', [
        param('^z+$', 'z' * 999, ['z' * 999], id='duplicated_z'),
        param('z+', 'X' + 'z' * 999 + 'X' + 'z' * 999, ['z' * 999, 'z' * 999], id='duplicated_z_2_times'),
        param('^(z+)+$', 'z' * 999, ['z' * 999], id='duplicated_z_evil_regex'),

    ])
    def test_split(self, expression, value, expected):
        assert sre.findall(expression, value) == expected
