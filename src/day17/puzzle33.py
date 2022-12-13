from src.data_parser import parser


def process_data(data):
    data = data[0].split(', ')
    x = [int(i) for i in data[0].split('x=')[1].split('..')]
    y = [int(i) for i in data[1][2:].split('..')]
    return x, y


def highest_y(data):
    y = process_data(data)[1]
    min_y = y[0]
    y = abs(min_y) - 1
    return (1 + y) * y // 2


if __name__ == '__main__':
    test_data = parser("input/day17_test")
    actual_data = parser("input/day17")

    print(highest_y(test_data))
    print(highest_y(actual_data))
