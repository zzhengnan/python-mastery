import inspect
from functools import wraps


class ValidatedFunction:
    def __init__(self, func):
        self.func = func
        self.sig = inspect.signature(self.func)
        self.annotations = self.func.__annotations__

    def __call__(self, *args, **kwargs):
        bound = self.sig.bind(*args, **kwargs)
        for param, arg in bound.arguments.items():
            validator = self.annotations[param]
            validator.check(arg)
        return self.func(*args, **kwargs)


class Validator:
    validators = {}
    @classmethod
    def __init_subclass__(cls):
        cls.validators[cls.__name__] = cls

    def __set_name__(self, cls, name):
        self.name = name

    def __set__(self, instance, value):
        instance.__dict__[self.name] = self.check(value)

    @classmethod
    def check(cls, value):
        return value


class Typed(Validator):
    expected_type = object
    @classmethod
    def check(cls, value):
        if not isinstance(value, cls.expected_type):
            raise TypeError(f'Expected {cls.expected_type!r}')
        return super().check(value)


_typed_classes = [
    ('Integer', int),
    ('Float', float),
    ('String', str),
]
globals().update({
    name: type(name, (Typed,), {'expected_type': expected_type})
    for name, expected_type in _typed_classes
})


class Positive(Validator):
    @classmethod
    def check(cls, value):
        if value < 0:
            raise ValueError('Expected >= 0')
        return super().check(value)


class NonEmpty(Validator):
    @classmethod
    def check(cls, value):
        if len(value) == 0:
            raise ValueError('Must be non-empty')
        return super().check(value)


class PositiveInteger(Integer, Positive):
    pass


class PositiveFloat(Float, Positive):
    pass


class NonEmptyString(String, NonEmpty):
    pass


def validated(func):
    sig = inspect.signature(func)
    arg_validators = dict(func.__annotations__)  # Make a copy
    return_validator = arg_validators.pop('return', None)

    @wraps(func)
    def wrapper(*args, **kwargs):
        bound = sig.bind(*args, **kwargs)

        # Check arguments
        arg_errors = []
        for param, validator in arg_validators.items():
            arg = bound.arguments[param]
            try:
                validator.check(arg)
            except TypeError as e:
                arg_errors.append(f'{param}: {e}')

        if arg_errors:
            raise TypeError('Bad arguments\n' + '\n'.join(arg_errors))

        # Check return value
        result = func(*args, **kwargs)
        if return_validator:
            try:
                return_validator.check(result)
            except TypeError as e:
                raise TypeError(f'Bad return: {e}')

        return result
    return wrapper


def enforce(**kwargs):
    arg_validators = dict(kwargs)
    return_validator = arg_validators.pop('return_',None)
    def decorator(func):
        sig = inspect.signature(func)
        @wraps(func)
        def wrapper(*args, **kwargs):
            bound = sig.bind(*args, **kwargs)

            arg_errors = []
            for param, validator in arg_validators.items():
                arg = bound.arguments[param]
                try:
                    validator.check(arg)
                except TypeError as e:
                    arg_errors.append(f'{param}: {e}')

            if arg_errors:
                raise TypeError('Bad arguments\n' + '\n'.join(arg_errors))

            # Check return value
            result = func(*args, **kwargs)
            if return_validator:
                try:
                    return_validator.check(result)
                except TypeError as e:
                    raise TypeError(f'Bad return: {e}')

            return result
        return wrapper
    return decorator


@validated
def add(x: Integer, y: Integer) -> Integer:
    return x + y


@enforce(x=Integer, y=Integer, return_=Integer)
def pow(x, y):
    return x ** y
