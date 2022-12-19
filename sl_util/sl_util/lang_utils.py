def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )

    cls.__str__ = __str__
    return cls


def auto_repr(cls):
    def __repr__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join("%s='%s'" % item for item in vars(self).items())
        )

    cls.__repr__ = __repr__
    return cls


def auto_eq(cls):
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False

        if self is other:
            return True

        return vars(self) == vars(other)

    cls.__eq__ = __eq__
    return cls
