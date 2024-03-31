from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import TypeVar

T = TypeVar('T')


class TableFormatter(ABC):
    _formats = {}

    def __init_subclass__(cls) -> None:
        name = cls.__module__.split('.')[-1]
        TableFormatter._formats[name] = cls

    @abstractmethod
    def headings(self, headers: Sequence[str]) -> None:
        """Display headings."""

    @abstractmethod
    def row(self, rowdata: Sequence[T]) -> None:
        """Display a single row of data."""


class ColumnFormatMixin:
    formats = []
    def row(self, rowdata):
        rowdata = [(fmt % d) for fmt, d in zip(self.formats, rowdata)]
        super().row(rowdata)


class UpperHeadersMixin:
    def headings(self, headers):
        headers = [header.upper() for header in headers]
        super().headings(headers)


def create_formatter(
    choice: str,
    column_formats: Sequence[str] | None = None,
    upper_headers: bool = False,
) -> TableFormatter:
    if choice not in TableFormatter._formats:
        __import__(f'{__package__}.formats.{choice}')
    formatter = TableFormatter._formats[choice]

    if column_formats:
        class formatter(ColumnFormatMixin, formatter):
            formats = column_formats

    if upper_headers:
        class formatter(UpperHeadersMixin, formatter):
            pass

    return formatter()


def print_table(
        records: Sequence[T],
        fields: Sequence[str],
        formatter: TableFormatter,
) -> None:
    # Print headers
    formatter.headings(fields)

    # Print actual values
    for record in records:
        rowdata = [getattr(record, field) for field in fields]
        formatter.row(rowdata)
