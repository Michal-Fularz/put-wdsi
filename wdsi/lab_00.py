import numpy as np


def main():
    # lists
    #    0  1  2  3
    l = [1, 2, 3, 4]
    # replace element
    l[0] = 10
    # replace slice
    l[1:3] = [20, 30]

    # dictionaries
    d = {
        'one': [1, 2],
        'two': [3, 5],
        'three': l,
    }

    # add new element
    d['four'] = [7, 11]

    # modify existing element
    d['one'] = [42, 1]

    # print an object with its name
    print(f'{d=}')

    # print dictionary as key-value pairs
    print(f'{d.items()=}')

    # find the key with the maximum sum of values
    max_sum = -np.inf
    max_key = None
    for key, value in d.items():
        print(f'{key=}, {value=}, {sum(value)=}')
        current_sum = sum(value)
        if current_sum > max_sum:
            max_sum = current_sum
            max_key = key
    print(f'Max key: {max_key} with sum {max_sum}')

    # same with lambda
    print("Using lambda:")
    print(max(d.items(), key=lambda x: sum(x[1])))


if __name__ == '__main__':
    main()
