from src.data_parser import parser


class Lanternfish:
    def __init__(self, days_left=8):
        self.days_left = days_left

    def get_days_left(self):
        return self.days_left

    def decrease_counter(self):
        self.days_left -= 1

    def spawn_fish(self):
        self.days_left = 6
        return Lanternfish()


class School:
    def __init__(self, fishes: list[Lanternfish]):
        self.fishes = fishes

    def growth_rate(self, days):
        fishes = self.fishes.copy()
        for day in range(days):
            new_fishes = []
            for fish in fishes:
                if fish.get_days_left() == 0:
                    new_fish = fish.spawn_fish()
                    new_fishes.append(new_fish)
                    continue
                fish.decrease_counter()
            fishes.extend(new_fishes)
        return len(fishes)


def growth_rate(data, days):
    data = data[0]
    data = [int(n) for n in data.split(',')]
    school = School([Lanternfish(n) for n in data])
    return school.growth_rate(days)


if __name__ == '__main__':
    test_data = parser("input/day6_test")
    actual_data = parser("input/day6")

    print(growth_rate(test_data, 80))
    print(growth_rate(actual_data, 80))
