from collections.abc import Callable
from functools import partial


def typedproperty(name: str, expected_type: type) -> Callable:
    private_name = '_' + name

    @property
    def value(self):
        return getattr(self, private_name)

    @value.setter
    def value(self, val):
        if not isinstance(val, expected_type):
            raise TypeError(f'Expected {expected_type}')
        setattr(self, private_name, val)

    return value


String = partial(typedproperty, expected_type=str)
Integer = partial(typedproperty, expected_type=int)
Float = partial(typedproperty, expected_type=float)
