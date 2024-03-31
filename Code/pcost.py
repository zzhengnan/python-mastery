def portfolio_cost(filename: str) -> float:
    total_cost = 0
    with open(filename) as f:
        for line in f:
            _, qty, price = line.split(' ')
            try:
                qty = int(qty)
                price = float(price)
            except ValueError as e:
                print(f'Could not parse {line!r}')
                print(f'Reason: {e}')
            else:
                total_cost += int(qty) * float(price)
    return total_cost
