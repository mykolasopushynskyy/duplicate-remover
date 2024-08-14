class Optional:
    _EMPTY = None  # Static element to hold the empty Optional

    def __init__(self, value=None):
        self._value = value

    @staticmethod
    def of(*args):
        if not isinstance(args, tuple):
            raise ValueError("Input must be a tuple")
        if any(item is None for item in args):
            return Optional.empty()
        return Optional(args)

    @staticmethod
    def empty():
        # Ensure that the empty Optional is created only once
        if Optional._EMPTY is None:
            Optional._EMPTY = Optional()
        return Optional._EMPTY

    def is_present(self):
        return self._value is not None

    def get(self):
        if self._value is None:
            raise ValueError("No value present")
        return self._value

    def or_else(self, other):
        return self._value if self._value is not None else other

    def or_else_get(self, supplier):
        return self._value if self._value is not None else supplier()

    def or_else_throw(self, exception):
        if self._value is None:
            raise exception
        return self._value

    def if_present(self, consumer: callable):
        if self._value is not None:
            consumer(*self._value)

    def transform(self, mapper: callable):
        if self._value is not None:
            return Optional.of(mapper(*self._value))
        return Optional.empty()
