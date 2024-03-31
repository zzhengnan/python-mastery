import csv
from ast import TypeVar
from collections.abc import Sequence
from functools import partial
from typing import Callable, NamedTuple

Constructor = TypeVar('T', bound=Callable)


def read(filename: str, constructor: Constructor) -> list[Constructor]:
    records = []
    with open(filename) as f:
        rows = csv.reader(f)
        _ = next(rows)     # Skip headers
        for row in rows:
            route, date, daytype, rides = row
            rides = int(rides)
            record = constructor(route, date, daytype, rides)
            records.append(record)
    return records


class RowClass:
    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides


class RowSlots:
    __slots__ = ('route', 'date', 'daytype', 'rides')

    def __init__(self, route, date, daytype, rides):
        self.route = route
        self.date = date
        self.daytype = daytype
        self.rides = rides


class RowTypedNamedTuple(NamedTuple):
    route: str
    date: str
    daytype: str
    rides: int


read_tuple = partial(
    read,
    constructor=lambda a, b, c, d: tuple((a, b, c, d))
)
read_dict = partial(
    read,
    constructor=lambda a, b, c, d: {'route': a, 'date': b, 'daytype': c, 'rides': d}
)
read_class = partial(read, constructor=RowClass)
read_namedtuple = partial(read, constructor=RowTypedNamedTuple)
read_slots = partial(read, constructor=RowSlots)
READERS = {
    'tuple': read_tuple,
    'dict': read_dict,
    'class': read_class,
    'namedtuple': read_namedtuple,
    'slots': read_slots,
}


class RideData(Sequence):
    def __init__(self):
        self.routes = []
        self.dates = []
        self.daytypes = []
        self.numrides = []

    def __len__(self):
        return len(self.routes)

    def __getitem__(self, index):
        if isinstance(index, int):
            return {
                'route': self.routes[index],
                'date': self.dates[index],
                'daytype': self.daytypes[index],
                'rides': self.numrides[index],
            }
        elif isinstance(index, slice):
            sliced = RideData()
            sliced.routes = self.routes[index]
            sliced.dates = self.dates[index]
            sliced.daytypes = self.daytypes[index]
            sliced.numrides = self.numrides[index]
            return sliced
        else:
            raise ValueError('Not supported')

    def append(self, d):
        self.routes.append(d['route'])
        self.dates.append(d['date'])
        self.daytypes.append(d['daytype'])
        self.numrides.append(d['rides'])


def read_columns(filename):
    '''
    Read the bus ride data into 4 lists, representing columns
    '''
    records = RideData()
    with open(filename) as f:
        rows = csv.reader(f)
        headings = next(rows)     # Skip headers
        for row in rows:
            record = {
                'route': row[0],
                'date': row[1],
                'daytype': row[2],
                'rides': int(row[3]),
            }
            records.append(record)
    return records
