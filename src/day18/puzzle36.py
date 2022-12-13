import copy

from src.data_parser import parser


class Pair:
    def __init__(self, left, right, nested_level=0, parent=None):
        self.parent_pair = parent
        self.nested_level = nested_level

        self.left = left
        if isinstance(left, Pair):
            left.add_parent(self)

        self.right = right
        if isinstance(right, Pair):
            right.add_parent(self)

    def add_pair(self, other_pair):
        pair = Pair(copy.deepcopy(self), copy.deepcopy(other_pair))
        pair.reduce_number()
        return pair

    def increase_nested_level(self):
        self.nested_level += 1

        if isinstance(self.left, Pair):
            self.left.increase_nested_level()

        if isinstance(self.right, Pair):
            self.right.increase_nested_level()

    def add_parent(self, parent):
        self.parent_pair = parent
        self.increase_nested_level()

    def get_magnitude(self):
        if isinstance(self.left, int):
            left = self.left
        else:
            left = self.left.get_magnitude()

        if isinstance(self.right, int):
            right = self.right
        else:
            right = self.right.get_magnitude()

        return 3 * left + 2 * right

    def explode_left(self):
        value = self.left
        pair = self
        while pair == pair.parent_pair.left:
            pair = pair.parent_pair
            if pair.parent_pair is None:
                return

        pair = pair.parent_pair

        if not isinstance(pair.left, int):
            pair = pair.left

            while not isinstance(pair.right, int):
                pair = pair.right

            pair.right += value

        else:
            pair.left += value

    def explode_right(self):
        value = self.right
        pair = self
        while pair == pair.parent_pair.right:
            pair = pair.parent_pair
            if pair.parent_pair is None:
                return

        pair = pair.parent_pair

        if not isinstance(pair.right, int):
            pair = pair.right

            while not isinstance(pair.left, int):
                pair = pair.left

            pair.left += value

        else:
            pair.right += value

    def explode(self):
        if self.nested_level != 4:
            return

        self.explode_left()
        self.explode_right()

        if self == self.parent_pair.left:
            self.parent_pair.left = 0
        else:
            self.parent_pair.right = 0

    def get_left_right(self, num):
        left = num // 2
        right = num - left
        return left, right

    def split_right(self):
        left, right = self.get_left_right(self.right)
        new_pair = Pair(left, right, self.nested_level + 1, self)
        self.right = new_pair
        new_pair.explode()

    def split_left(self):
        left, right = self.get_left_right(self.left)
        new_pair = Pair(left, right, self.nested_level + 1, self)
        self.left = new_pair
        new_pair.explode()

    def reduce_number(self):
        self.explode_number()

        flag = 1
        while flag == 1:
            flag = self.split_number()

    def explode_number(self):
        self.explode()

        if isinstance(self.left, Pair):
            self.left.explode_number()

        if isinstance(self.right, Pair):
            self.right.explode_number()

    def split_number(self):
        if isinstance(self.left, Pair):

            if self.left.split_number() == 1:
                return 1

        elif self.left >= 10:
            self.split_left()
            return 1

        if isinstance(self.right, Pair):

            if self.right.split_number() == 1:
                return 1

        elif self.right >= 10:
            self.split_right()
            return 1

    def print_number(self, out=''):
        if isinstance(self.left, Pair):
            out = self.left.print_number() + out
        else:
            out = str(self.left) + out

        out += ','

        if isinstance(self.right, Pair):
            out += self.right.print_number()
        else:
            out += str(self.right)

        out = '[' + out + ']'

        return out


class PairCreator:
    def __init__(self, number):
        self.number = number

    def make_pair(self, data):
        left = data[1]
        if isinstance(left, str):
            left = int(left)

        right = data[3]
        if isinstance(right, str):
            right = int(right)

        return Pair(left, right)

    def get_starting_idx(self, ending_idx):
        for i in range(ending_idx, -1, -1):
            if self.number[i] == '[':
                return i

    def get_pair(self):

        pair = None

        while self.number.count(']'):

            ending_idx = self.number.index(']')
            starting_idx = self.get_starting_idx(ending_idx)

            pair = self.make_pair(self.number[starting_idx:ending_idx + 1])

            del self.number[starting_idx:ending_idx + 1]
            self.number.insert(starting_idx, pair)

        return pair


def process_data(data: list[str, str, ...]):
    return [PairCreator(list(number)).get_pair() for number in data]


def largest_magnitude(data):
    pairs = process_data(data)
    max_magnitude = 0

    for p1 in pairs:
        for p2 in pairs:

            if p1 == p2:
                continue

            p = p1.add_pair(p2)
            mag = p.get_magnitude()

            if mag > max_magnitude:
                max_magnitude = mag

    return max_magnitude


if __name__ == '__main__':
    test_data = parser("input/day18_test")
    actual_data = parser("input/day18")

    print(largest_magnitude(test_data))
    print(largest_magnitude(actual_data))
