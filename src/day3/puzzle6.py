from src.data_parser import parser


def most_common(bits):
    ones = bits.count('1')
    zeros = len(bits) - ones
    return '1' if ones >= zeros else '0'


def least_common(bits):
    ones = bits.count('1')
    zeros = len(bits) - ones
    return '0' if zeros <= ones else '1'


def get_rate(data, rate_type):
    c = 0
    while len(data) != 1:
        bits = [num[c] for num in data]
        if rate_type == 'oxygen':
            bit = most_common(bits)
        else:
            bit = least_common(bits)
        data = [num for num in data if num[c] == bit]
        c += 1
    return int(data[0], 2)


def life_support_rating(data):
    oxygen = get_rate(data, 'oxygen')
    co2 = get_rate(data, 'co2')
    return oxygen * co2


if __name__ == '__main__':
    test_data = parser("input/day3_test")
    actual_data = parser("input/day3")

    print(life_support_rating(test_data))
    print(life_support_rating(actual_data))
