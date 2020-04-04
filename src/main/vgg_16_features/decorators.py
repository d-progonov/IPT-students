def lazy(func):
    @property
    def wrapper(self):
        attr_name = '__%s' % func.__name__
        try:
            value = getattr(self, attr_name)
        except AttributeError:
            value = func(self)
            setattr(self, attr_name, value)
        return value

    return wrapper