import re2


class SecureRegexWrapper:

    @staticmethod
    def match(expression, value, options=None):
        return re2.match(expression, value, options)

    @staticmethod
    def sub(pattern, replace, string, count=0, flags=0):
        return re2.sub(pattern, replace, string, count, flags)

    @staticmethod
    def escape(pattern):
        return re2.escape(pattern)

    @classmethod
    def findall(cls, regex, string, options=None):
        return re2.findall(regex, string, options)

    @classmethod
    def split(cls, pattern, text, maxsplit=0, options=None):
        return re2.split(pattern, text, maxsplit, options)
