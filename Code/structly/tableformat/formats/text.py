from ..formatter import TableFormatter


class TextTableFormatter(TableFormatter):
    """
          name     shares      price
    ---------- ---------- ----------
            AA        100       32.2
           IBM         50       91.1
           CAT        150      83.44
          MSFT        200      51.23
            GE         95      40.37
          MSFT         50       65.1
           IBM        100      70.44
    """
    def headings(self, headers):
        print(' '.join(f'{header:>10}' for header in headers))
        print(('-' * 10 + ' ') * len(headers))

    def row(self, rowdata):
        print(' '.join(f'{datum:>10}' for datum in rowdata))
