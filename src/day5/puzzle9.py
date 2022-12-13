from src.data_parser import parser


def count_points(data):
    data = prepare_data(data)
    points = dict()
    for line in data:
        x1, y1 = line[0]
        x2, y2 = line[1]
        if x1 == x2:
            for i in range(min(y1, y2), max(y1, y2) + 1):
                points.setdefault((x1, i), 0)
                points[(x1, i)] += 1
        elif y1 == y2:
            for i in range(min(x1, x2), max(x1, x2) + 1):
                points.setdefault((i, y1), 0)
                points[(i, y1)] += 1
    return sum(n > 1 for n in points.values())


def prepare_data(data: list[str]):
    lines = []
    for line in data:
        lines.append([[int(coord) for coord in coords.split(',')] for coords in line.split(' -> ')])
    return lines


if __name__ == '__main__':
    test_data = parser("input/day5_test")
    actual_data = parser("input/day5")

    print(count_points(test_data))
    print(count_points(actual_data))
