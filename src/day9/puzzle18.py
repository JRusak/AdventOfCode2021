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

    def mark_out(self):
        self.marked = False


class HeightMap:
    def __init__(self, points: list[list[Point]]):
        self.points = points
        self.X = len(points[0])
        self.Y = len(points)
        self.low_points = self.get_low_points()
        self.basins_sizes = self.get_basins_sizes()

    def print_map(self):
        out = ''
        for row in range(self.Y):
            for col in range(self.X):
                point = self.points[row][col]
                if point.is_marked():
                    out += 'o'
                else:
                    out += 'x'
            out += '\n'
        print(out)

    def get_basins_sizes(self):
        basins_sizes = []
        for low_point in self.low_points:
            basins_sizes.append(self.basin_size(low_point))
        return basins_sizes

    def basin_size(self, point, size=1):
        point.mark()
        points = self.get_adjacent_points(point)
        for p in points:
            if not p.is_marked() and p.value < 9:
                size += self.basin_size(p)
        return size

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
        self.mark_out_all_points()
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

    def mark_out_all_points(self):
        for row in range(self.Y):
            for col in range(self.X):
                point = self.points[row][col]
                point.mark_out()


def process_data(data):
    data = [[int(n) for n in line.strip()] for line in data]
    points = []
    for row in range(len(data)):
        r = []
        for col in range(len(data[0])):
            r.append(Point(data[row][col], row, col))
        points.append(r)
    return HeightMap(points)


def basins_number(data):
    h_map = process_data(data)
    b1, b2, b3 = sorted(h_map.basins_sizes, reverse=True)[:3]
    return b1 * b2 * b3


if __name__ == '__main__':
    test_data = parser("input/day9_test")
    actual_data = parser("input/day9")

    print(basins_number(test_data))
    print(basins_number(actual_data))
