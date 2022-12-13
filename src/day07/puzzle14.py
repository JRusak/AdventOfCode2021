from src.data_parser import parser


def needed_fuel(data):
    data = process_data(data)

    i = min(data)
    j = max(data)
    min_fuel = float('inf')

    for pos in range(i, j + 1):
        fuel = 0
        for num in data:
            n = abs(num - pos)
            fuel += (1 + n) * n // 2
            if fuel > min_fuel:
                fuel = None
                break
        if fuel:
            min_fuel = fuel

    return min_fuel


def process_data(data):
    return [int(n) for n in data[0].split(',')]


if __name__ == '__main__':
    test_data = parser("input/day7_test")
    actual_data = parser("input/day7")

    print(needed_fuel(test_data))
    print(needed_fuel(actual_data))
