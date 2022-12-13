from src.data_parser import parser


def most_common(bits):
    ones = bits.count('1')
    zeros = len(bits) - ones
    return 1 if ones > zeros else 0


def power_consumption(data):
    columns = zip(*data)

    gamma = ''
    epsilon = ''

    for col in columns:

        bit = most_common(col)
        if bit == 1:
            gamma += '1'
            epsilon += '0'
        elif bit == 0:
            gamma += '0'
            epsilon += '1'
    return int(gamma, 2) * int(epsilon, 2)


if __name__ == '__main__':
    test_data = parser("input/day3_test")
    actual_data = parser("input/day3")

    print(power_consumption(test_data))
    print(power_consumption(actual_data))
