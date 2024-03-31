from collections.abc import Sequence
from decimal import Decimal
from typing import Self

from validate import NonEmptyString, PositiveFloat, PositiveInteger


class Stock:
    _types = (str, int, float)  # Used in `from_row`

    name = NonEmptyString()
    shares = PositiveInteger()
    price = PositiveFloat()

    def __init__(self, name: str, shares: int, price: float) -> None:
        self.name = name
        self.shares = shares
        self.price = price

    def __repr__(self) -> str:
        return f'Stock(name={self.name!r}, shares={self.shares!r}, price={self.price!r})'

    def __eq__(self, other) -> bool:
        return (
            isinstance(other, Stock) and
            self.name == other.name and
            self.shares == other.shares and
            self.price == other.price
        )

    @classmethod
    def from_row(cls, row: Sequence[str]) -> Self:
        values = (func(value) for func, value in zip(cls._types, row))
        return cls(*values)

    @property
    def cost(self) -> float:
        return self.shares * self.price

    def sell(self, shares: int) -> None:
        self.shares -= shares


class DStock(Stock):
    _types = (str, int, Decimal)


def print_portfolio(portfolio: Sequence) -> None:
    print(f'{"name":>10} {"shares":>10} {"price":>10}')
    print('-' * 10, '-' * 10, '-' * 10)
    for s in portfolio:
        print(f'{s.name:>10} {s.shares:>10} {s.price:>10}')
