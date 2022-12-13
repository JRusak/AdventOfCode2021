from src.data_parser import parser
from puzzle3 import process


def count_dist_mul_depth(data: list[list[str, str]]):
    depth = horizontal_position = aim = 0
    for direction, value in data:
        value = int(value)
        if direction == 'forward':
            horizontal_position += value
            depth += aim * value
        elif direction == 'up':
            aim -= value
        elif direction == 'down':
            aim += value
    return depth * horizontal_position


if __name__ == '__main__':
    test_data = parser("input/day2_test")
    actual_data = parser("input/day2")

    print(count_dist_mul_depth(process(test_data)))
    print(count_dist_mul_depth(process(actual_data)))
