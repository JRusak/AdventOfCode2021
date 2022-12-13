from src.data_parser import parser


class Point:
    def __init__(self, value: int, row: int, col: int):
        self.value = value
        self.row = row
        self.col = col
        self.marked = False

    def is_marked(self) -> bool:
        return self.marked

    def mark(self) -> None:
        self.marked = True


class HeightMap:
    def __init__(self, points: list[list[Point]]):
        self.points = points
        self.X = len(points[0])
        self.Y = len(points)
        self.low_points = self.get_low_points()

    def get_low_points(self) -> list[Point]:
        low_points = []
        for row in range(self.Y):
            for col in range(self.X):
                point = self.points[row][col]

                if point.is_marked():
                    continue

                low_point = self.find_low_point(point)
                if low_point not in low_points:
                    low_points.append(low_point)
        return low_points

    def find_low_point(self, point: Point) -> Point:
        point.mark()
        adjacent_points = self.get_adjacent_points(point)
        v_p = {p.value: p for p in adjacent_points}
        if point.value < min(v_p.keys()):
            return point
        new_point = v_p[min(v_p.keys())]
        return self.find_low_point(new_point)

    def get_adjacent_points(self, point: Point) -> list[Point]:
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        pos = point.row, point.col

        adjacent_points = []
        for move in moves:
            n_pos = pos[0] + move[0], pos[1] + move[1]
            if not self.check_pos(n_pos):
                continue
            row, col = n_pos
            point = self.points[row][col]
            adjacent_points.append(point)
        return adjacent_points

    def check_pos(self, pos: tuple[int, int]) -> bool:
        return 0 <= pos[0] < self.Y and 0 <= pos[1] < self.X

    def risk_level(self):
        return sum(p.value + 1 for p in self.low_points)


def process_data(data):
    data = [[int(n) for n in line.strip()] for line in data]
    points = []
    for row in range(len(data)):
        r = []
        for col in range(len(data[0])):
            r.append(Point(data[row][col], row, col))
        points.append(r)
    return HeightMap(points)


def get_risk_level(data):
    h_map = process_data(data)
    return h_map.risk_level()


if __name__ == '__main__':
    test_data = parser("input/day9_test")
    actual_data = parser("input/day9")

    print(get_risk_level(test_data))
    print(get_risk_level(actual_data))
