import numpy as np


def main():
    l = [1, 2, 3, 4]

    d = {
        'one': [1, 2],
        'two': [3, 5],
    }

    d['three'] = [7, 9]

    print(f'{d=}')
    print(f'{d.items()=}')
    print(max(d.items(), key=lambda x: sum(x[1])))


if __name__ == '__main__':
    main()
