import os
import time
from functools import wraps


def follow(fname, target):
    with open(fname) as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if line == '':
                time.sleep(.1)
            else:
                target.send(line)


def consumer(func):
    @wraps(func)
    def start(*args, **kwargs):
        coro = func(*args, **kwargs)
        coro.send(None)
        return coro
    return start


@consumer
def printer():
    while True:
        try:
            line = yield
            print(line)
        except Exception as e:
            print(f'ERROR: {e!r}')


def receive(expected_type):
    msg = yield
    assert isinstance(msg, expected_type), f'Expected type {expected_type}'
    return msg


if __name__ == '__main__':
    follow('../Data/stocklog.csv', printer())
