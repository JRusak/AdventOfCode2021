from src.data_parser import parser


def process_example_data(data):
    data = [d.strip().split() for d in data[1::2]]
    return data


def process_data(data):
    data = [d.split('|')[1].strip().split() for d in data]
    return data


def unique_combinations(data):
    return sum(sum(len(word) in (2, 3, 4, 7) for word in d) for d in data)


if __name__ == '__main__':
    test_data = parser("input/day8_test")
    actual_data = parser("input/day8")

    new_test_data = process_example_data(test_data)
    new_actual_data = process_data(actual_data)

    print(unique_combinations(new_test_data))
    print(unique_combinations(new_actual_data))
