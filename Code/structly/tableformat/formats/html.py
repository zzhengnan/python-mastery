from ..formatter import TableFormatter


class HTMLTableFormatter(TableFormatter):
    """
    <tr> <th>name</th> <th>shares</th> <th>price</th> </tr>
    <tr> <td>AA</td> <td>100</td> <td>32.2</td> </tr>
    <tr> <td>IBM</td> <td>50</td> <td>91.1</td> </tr>
    <tr> <td>CAT</td> <td>150</td> <td>83.44</td> </tr>
    <tr> <td>MSFT</td> <td>200</td> <td>51.23</td> </tr>
    <tr> <td>GE</td> <td>95</td> <td>40.37</td> </tr>
    <tr> <td>MSFT</td> <td>50</td> <td>65.1</td> </tr>
    <tr> <td>IBM</td> <td>100</td> <td>70.44</td> </tr>
    """
    def headings(self, headers):
        print(
            '<tr> ' +
            f' '.join(f'<th>{header}</th>' for header in headers) +
            ' </tr>'
        )

    def row(self, rowdata):
        print(
            '<tr> ' +
            f' '.join(f'<td>{str(datum)}</td>' for datum in rowdata) +
            ' </tr>'
        )
