import csv
import logging
from collections.abc import Callable, Sequence
from typing import Any

__all__ = ['read_csv_as_dicts', 'read_csv_as_instances']

LOGGER = logging.getLogger(__name__)

Lines = Sequence[str]
Headers = Sequence[str] | None


def convert_csv(
    lines: Lines,
    converter: Callable[[Sequence[str], Sequence[str]], Any],
    headers: Headers,
):
    rows = csv.reader(lines)
    start_row = 0
    if headers is None:
        headers = next(rows)
        start_row += 1
    records = []
    for i, row in enumerate(rows, start=start_row):
        try:
            record = converter(headers, row)
        except ValueError as e:
            LOGGER.warning(f'Row {i} is bad: {row}')
            LOGGER.debug(f'Reason: {e}')
        else:
            records.append(record)
    return records


def csv_as_dicts(
    lines: Lines,
    types: Sequence[type],
    headers: Headers,
):
    def to_dict(keys: Sequence[str], row: Sequence[str]):
        return {
            key: func(value)
            for key, func, value in zip(keys, types, row)
        }
    return convert_csv(lines, to_dict, headers)


def csv_as_instances(
    lines: Lines,
    cls: type,
    headers: Headers,
):
    return convert_csv(
        lines,
        lambda _, row: cls.from_row(row),
        headers,
    )


def read_csv_as_dicts(
    filename: str,
    types: Sequence[type],
    *,
    headers: Headers = None,
) -> list[dict]:
    """Read CSV into list of dicts with optional type conversion."""
    with open(filename) as lines:
        return csv_as_dicts(lines, types, headers)


def read_csv_as_instances(
    filename: str,
    cls: type,
    *,
    headers: Headers = None,
) -> list[type]:
    """Read CSV into list of instances."""
    with open(filename) as lines:
        return csv_as_instances(lines, cls, headers)
