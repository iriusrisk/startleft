import re2


def match(expression, value, options=None):
    return re2.match(expression, value, options)


def sub(pattern, replace, string, count=0, flags=0):
    return re2.sub(pattern, replace, string, count, flags)


def escape(pattern):
    return re2.escape(pattern)


def findall(regex, string, options=None):
    return re2.findall(regex, string, options)


def split(pattern, text, maxsplit=0, options=None):
    return re2.split(pattern, text, maxsplit, options)


def compile(pattern, options=None):
    return re2.compile(pattern, options)


def search(pattern, string, options=None):
    return re2.search(pattern, string, options)
