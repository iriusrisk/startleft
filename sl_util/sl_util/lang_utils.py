def auto_repr(cls):
    def __repr__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join("%s='%s'" % item for item in vars(self).items())
        )

    cls.__repr__ = __repr__
    return cls
