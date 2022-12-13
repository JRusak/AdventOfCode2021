from src.data_parser import parser


def process(data):
    return [x.split() for x in data]


def count_dist_mul_depth(data: list[list[str, str]]):
    depth = horizontal_position = 0
    for direction, value in data:
        value = int(value)
        if direction == 'forward':
            horizontal_position += value
        elif direction == 'up':
            depth -= value
        elif direction == 'down':
            depth += value
    return depth * horizontal_position


if __name__ == '__main__':
    test_data = parser("input/day2_test")
    actual_data = parser("input/day2")

    print(count_dist_mul_depth(process(test_data)))
    print(count_dist_mul_depth(process(actual_data)))
