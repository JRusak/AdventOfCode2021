import queue

from src.data_parser import parser


def process_data(data):
    return [line.rstrip() for line in data]


POINTS = {')': 3, ']': 57, '}': 1197, '>': 25137}
CLOSING_CHUNKS = {'(': ')', '[': ']', '{': '}', '<': '>'}


class Buffor:
    def __init__(self):
        self.opening_chunks = queue.LifoQueue()
        self.wrong_closings = dict()

    def check_chunk(self, chunk):
        q = self.opening_chunks
        if chunk in ('(', '[', '{', '<'):
            q.put(chunk)
        elif CLOSING_CHUNKS[q.queue[-1]] == chunk:
            q.get()
        else:
            self.wrong_closings.setdefault(chunk, 0)
            self.wrong_closings[chunk] += 1
            return 1

    def count_points(self):
        return sum(POINTS[chunk] * num for chunk, num in self.wrong_closings.items())

    def clear_buff(self):
        self.opening_chunks = queue.LifoQueue()


def count_points(data):
    data = process_data(data)
    buf = Buffor()
    for line in data:
        for chunk in line:
            if buf.check_chunk(chunk) == 1:
                break
        buf.clear_buff()
    return buf.count_points()


if __name__ == '__main__':
    test_data = parser("input/day10_test")
    actual_data = parser("input/day10")

    print(count_points(test_data))
    print(count_points(actual_data))
