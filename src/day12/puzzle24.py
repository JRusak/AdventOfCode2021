from src.data_parser import parser


class Cave:
    def __init__(self, name: str):
        self.name = name
        self.connected_caves = None
        self.visited = False
        self.special_cave = False

    def add_caves(self, caves):
        self.connected_caves = sorted(caves, key=lambda x: x.name)

    def is_marked(self):
        return self.visited

    def is_upper(self):
        return self.name.isupper()

    def mark(self):
        self.visited = True

    def reset(self):
        self.visited = False


class PathFinder:
    def __init__(self, start: Cave, end: Cave):
        self.start = start
        self.end = end
        self.paths = 0
        self.is_special_cave = False

    def find_all_paths(self):
        self.find_end(self.start)
        return self.paths

    def find_end(self, cave: Cave):
        for c in cave.connected_caves:
            if c == self.end:
                self.paths += 1
                continue
            if c.is_marked() and not c.is_upper() and self.is_special_cave:
                continue
            elif c.is_marked() and not c.is_upper() and not self.is_special_cave:
                self.toggle_special_cave(c)
            c.mark()
            self.find_end(c)
            if c.special_cave:
                self.toggle_special_cave(c)
            else:
                c.reset()

    def toggle_special_cave(self, cave: Cave):
        cave.special_cave = not cave.special_cave
        self.is_special_cave = not self.is_special_cave


def process_data(data: list[str]):
    d = dict()
    caves = dict()
    for line in data:
        k, v = line.strip().split('-')
        d.setdefault(k, set())
        d.setdefault(v, set())
        caves.setdefault(k, Cave(k))
        caves.setdefault(v, Cave(v))
        if k != 'end' and v != 'start':
            d[k].add(caves[v])
        if k != 'start' and v != 'end':
            d[v].add(caves[k])

    start, end = None, None
    for name, cave in caves.items():
        if name == 'start':
            start = cave
        elif name == 'end':
            end = cave
        cave.add_caves(d[name])

    return start, end


def paths_number(data):
    start, end = process_data(data)
    pf = PathFinder(start, end)
    return pf.find_all_paths()


if __name__ == '__main__':
    test_data = parser("input/day12_test")
    actual_data = parser("input/day12")

    print(paths_number(test_data))
    print(paths_number(actual_data))
