from logcall import logformat, logged


@logged
def add(x, y):
    """Add two things."""
    return x + y


@logformat('{func.__code__.co_filename}:{func.__name__}')
def mul(x, y):
    """Multiply two things."""
    return x * y
