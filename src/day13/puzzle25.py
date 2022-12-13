from src.data_parser import parser
from collections import deque
from typing import Deque


class FoldInstruction:
    def __init__(self, dir_line):
        self.direction = dir_line[0]
        self.line = int(dir_line[1])


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.marked = False

    def mark(self):
        self.marked = True

    def is_marked(self):
        return self.marked


class TransparentPaper:
    def __init__(self, points: list[list[Point]], fold_instructions: Deque[FoldInstruction]):
        self.points = points
        self.fold_instructions = fold_instructions
        self.X = len(points[0])
        self.Y = len(points)

    def fold(self):
        instruction = self.fold_instructions.popleft()
        line = instruction.line
        if instruction.direction == 'x':
            new_points = []
            remaining_points = []
            for ln in self.points:
                new_points.append(ln[:line])
                remaining_points.append(ln[line + 1:])
            for tup in zip(remaining_points, new_points):
                for old, new in zip(tup[0], tup[1][::-1]):
                    if old.is_marked() or new.is_marked():
                        new.mark()
            self.X = len(new_points[0])
        else:
            new_points = self.points[:line]
            remaining_points = self.points[line + 1:]
            for tup in zip(remaining_points, new_points[::-1]):
                for old, new in zip(*tup):
                    if old.is_marked() or new.is_marked():
                        new.mark()
            self.Y = len(new_points)
        self.points = new_points

    def count_marked_points(self):
        return sum(self.points[row][col].is_marked() for col in range(self.X) for row in range(self.Y))


def process_data(data: list[str]):
    idx = data.index('\n')
    d1 = data[:idx]
    coordinates = [[int(n) for n in line.strip().split(',')] for line in d1]
    max_x = max(coordinates, key=lambda x: x[0])[0]
    max_y = max(coordinates, key=lambda x: x[1])[1]
    points = []
    for row in range(max_y + 1):
        new_r = []
        for col in range(max_x + 1):
            point = Point(col, row)
            if [col, row] in coordinates:
                point.mark()
            new_r.append(point)
        points.append(new_r)

    d2 = data[idx + 1:]
    instructions = deque([FoldInstruction(line.split()[-1].strip().split('=')) for line in d2])

    return points, instructions


def count_points(data):
    points, instructions = process_data(data)
    tp = TransparentPaper(points, instructions)
    tp.fold()
    return tp.count_marked_points()


if __name__ == '__main__':
    test_data = parser("input/day13_test")
    actual_data = parser("input/day13")

    print(count_points(test_data))
    print(count_points(actual_data))
