from src.data_parser import parser


class FishGroup:
    def __init__(self, num_of_fishes=0):
        self.num_of_fishes = num_of_fishes
        self.prev = None
        self.next = None


class School:
    def __init__(self, head: FishGroup, tail: FishGroup):
        self.head = head
        self.tail = tail

    def growth_rate(self, days):
        h = self.head
        t = self.tail

        for _ in range(days):
            val = h.num_of_fishes
            h = h.next
            t = t.next
            t.prev.prev.num_of_fishes += val

        fishes = 0
        g = h
        while g != t:
            fishes += g.num_of_fishes
            g = g.next
        fishes += t.num_of_fishes
        return fishes


def growth_rate(data, days):
    data = data[0]

    head = FishGroup()
    prev_group = head
    for i in range(1, 9):
        group = FishGroup(data.count(str(i)))
        prev_group.next = group
        group.prev = prev_group
        prev_group = group
    tail = prev_group
    tail.next = head
    head.prev = tail

    school = School(head, tail)
    return school.growth_rate(days)


if __name__ == '__main__':
    test_data = parser("input/day6_test")
    actual_data = parser("input/day6")

    print(growth_rate(test_data, 256))
    print(growth_rate(actual_data, 256))

