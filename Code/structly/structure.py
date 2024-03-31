import sys
from collections import ChainMap

from .validate import Validator, validated

__all__ = ['Structure']


class StructureMeta(type):
    @classmethod
    def __prepare__(meta, clsname, bases):
        return ChainMap({}, Validator.validators)

    @staticmethod
    def __new__(meta, name, bases, methods):
        methods = methods.maps[0]
        return super().__new__(meta, name, bases, methods)


def validate_attributes(cls: type) -> type:
    _fields = []
    _types = []

    for key, value in vars(cls).items():
        if isinstance(value, Validator):
            _fields.append(key)
            _types.append(value.expected_type)
        elif callable(value) and value.__annotations__:
            setattr(cls, key, validated(value))

    cls._fields = tuple(_fields)
    cls._types = tuple(_types)

    if cls._fields:
        cls.create_init()
    return cls


class Structure(metaclass=StructureMeta):
    _fields = ()
    _types = ()

    @classmethod
    def __init_subclass__(cls):
        validate_attributes(cls)

    def __iter__(self):
        for name in self._fields:
            yield getattr(self, name)

    def __eq__(self, other):
        return type(self) is type(other) and tuple(self) == tuple(other)

    @classmethod
    def from_row(cls, row):
        data = [func(val) for func, val in zip(cls._types, row)]
        return cls(*data)

    @classmethod
    def create_init(cls):
        args = ', '.join(cls._fields)
        code = f'def __init__(self, {args}):\n'
        for field in cls._fields:
            code += f'    self.{field} = {field}\n'
        locs = {}
        exec(code, locs)
        cls.__init__ = locs['__init__']

    @staticmethod
    def _init():
        locs = sys._getframe(1).f_locals
        self = locs.pop('self')
        for name, val in locs.items():
            setattr(self, name, val)

    def __setattr__(self, name, value):
        if name not in self._fields and not name.startswith('_'):
            raise AttributeError(f'No attribute {name!r}')
        super().__setattr__(name, value)

    def __repr__(self):
        cls_name = type(self).__name__
        field_values = ', '.join(repr(getattr(self, field)) for field in self._fields)
        return f'{cls_name}({field_values})'


def typed_structure(clsname, **validators):
    cls = type(clsname, (Structure,), validators)
    return cls
