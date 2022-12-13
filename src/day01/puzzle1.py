from src.data_parser import parser


def process(data):
    return [int(x) for x in data]


def increases_counter(data: list[int]) -> int:
    counter = 0
    prev = data[0]
    for n in data[1:]:
        if prev < n:
            counter += 1
        prev = n
    return counter


if __name__ == '__main__':
    test_data = parser("input/day1_test")
    actual_data = parser("input/day1")

    print(increases_counter(process(test_data)))
    print(increases_counter(process(actual_data)))
