from functools import wraps


def logformat(fmt):
    def logged(func):
        print(f'Adding logging to {func.__name__!r}')
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(fmt.format(func=func))
            return func(*args, **kwargs)
        return wrapper
    return logged


logged = logformat('Calling {func.__name__!r}')
