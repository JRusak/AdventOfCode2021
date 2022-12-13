from src.data_parser import parser
from puzzle1 import process, increases_counter


def get_group_scores(data: list[int], group_len) -> list[int]:
    new_data = []
    for i in range(len(data) - group_len + 1):
        new_data.append(sum(data[i:i + group_len]))
    return new_data


if __name__ == '__main__':
    test_data = parser("input/day1_test")
    actual_data = parser("input/day1")

    new_test_data = get_group_scores(process(test_data), 3)
    new_actual_data = get_group_scores(process(actual_data), 3)

    print(increases_counter(new_test_data))
    print(increases_counter(new_actual_data))

