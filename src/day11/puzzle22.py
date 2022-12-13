from src.data_parser import parser


class Octopus:
    def __init__(self, energy, row, col):
        self.energy_level = energy
        self.row = row
        self.col = col
        self.flushed = False
        self.marked = False

    def increase_energy_level(self):
        if not self.flushed:
            self.energy_level += 1

    def has_flushed(self):
        return self.flushed

    def update_energy(self):
        self.increase_energy_level()
        if self.energy_level > 9:
            self.flushed = True
            self.energy_level = 0

    def rest(self):
        self.flushed = False
        self.marked = False

    def mark(self):
        self.marked = True

    def is_marked(self):
        return self.marked


class Cavern:
    def __init__(self, octopus_grid):
        self.octopus_grid = octopus_grid
        self.rows = len(octopus_grid)
        self.cols = len(octopus_grid[0])
        self.octopus_number = self.rows * self.cols
        self.flushes = 0

    def update(self) -> None:
        for row in range(self.rows):
            for col in range(self.cols):
                octopus = self.octopus_grid[row][col]
                octopus.update_energy()
                self.flush(octopus)
        self.reset()

    def reset(self):
        for row in range(self.rows):
            for col in range(self.cols):
                octopus = self.octopus_grid[row][col]
                octopus.rest()

    def get_adjacents(self, octopus: Octopus) -> list[Octopus]:
        shifts = [(-1, -1), (0, -1), (1, -1), (-1, 0),
                  (1, 0), (-1, 1), (0, 1), (1, 1)]
        adjacents = []
        for shift in shifts:
            r, c = shift
            new_row = octopus.row + r
            new_col = octopus.col + c
            if self.in_bounds(new_row, new_col):
                adjacents.append(self.octopus_grid[new_row][new_col])
        return adjacents

    def in_bounds(self, new_row: int, new_col: int) -> bool:
        return 0 <= new_row < self.rows and 0 <= new_col < self.cols

    def flush(self, octopus: Octopus):
        if not octopus.has_flushed() or (octopus.has_flushed() and octopus.is_marked()):
            return
        self.flushes += 1
        octopus.mark()
        adjacents = self.get_adjacents(octopus)
        for neigh_octopus in adjacents:
            neigh_octopus.update_energy()
            self.flush(neigh_octopus)

    def get_flushes(self, n):
        for _ in range(n):
            self.update()
        return self.flushes

    def get_flushed_step(self):
        flushed_num = prev_flushes = 0
        c = 0
        while flushed_num != self.octopus_number:
            self.update()
            flushed_num = self.flushes - prev_flushes
            prev_flushes = self.flushes
            c += 1
        return c


def process_data(data):
    data = [[int(n) for n in line.strip()] for line in data]
    n_data = []
    for row in range(len(data)):
        n_row = []
        for col in range(len(data[0])):
            energy = data[row][col]
            n_row.append(Octopus(energy, row, col))
        n_data.append(n_row)
    return n_data


def get_step(data):
    data = process_data(data)
    grid = Cavern(data)
    return grid.get_flushed_step()


if __name__ == '__main__':
    test_data = parser("input/day11_test")
    actual_data = parser("input/day11")

    print(get_step(test_data))
    print(get_step(actual_data))
