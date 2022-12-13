import queue

from src.data_parser import parser


def process_data(data):
    return [line.rstrip() for line in data]


POINTS = {')': 1, ']': 2, '}': 3, '>': 4}
CLOSING_CHUNKS = {'(': ')', '[': ']', '{': '}', '<': '>'}


class Buffor:
    def __init__(self):
        self.opening_chunks = queue.LifoQueue()
        self.scores = []

    def check_chunk(self, chunk):
        q = self.opening_chunks
        if chunk in ('(', '[', '{', '<'):
            q.put(chunk)
        elif CLOSING_CHUNKS[q.queue[-1]] == chunk:
            q.get()
        else:
            return 1

    def save_score(self):
        score = 0
        q = self.opening_chunks
        while not q.empty():
            chunk = CLOSING_CHUNKS[q.get()]
            score *= 5
            score += POINTS[chunk]
        self.scores.append(score)

    def get_middle_score(self):
        s = sorted(self.scores)
        return s[len(s) // 2]

    def clear_buff(self):
        self.opening_chunks = queue.LifoQueue()


def middle_score(data):
    data = process_data(data)
    buf = Buffor()
    for line in data:
        b = False
        for chunk in line:
            if buf.check_chunk(chunk) == 1:
                buf.clear_buff()
                b = True
                break
        if b:
            continue
        buf.save_score()
        buf.clear_buff()
    return buf.get_middle_score()


if __name__ == '__main__':
    test_data = parser("input/day10_test")
    actual_data = parser("input/day10")

    print(middle_score(test_data))
    print(middle_score(actual_data))

