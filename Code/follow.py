import os
import time


def follow(fname):
    try:
        with open(fname) as f:
            f.seek(0, os.SEEK_END)
            while True:
                line = f.readline()
                if line == '':
                    time.sleep(.1)
                    continue
                yield line
    except GeneratorExit:
        print('Following done')


if __name__ == '__main__':
    for line in follow('../Data/stocklog.csv'):
        fields = line.split(',')
        name = fields[0].strip('"')
        price = float(fields[1])
        change = float(fields[4])
        if change < 0:
            print(f'{name:>10s} {price:>10.2f} {change:>10.2f}')
