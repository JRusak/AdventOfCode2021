from src.data_parser import parser


class Field:
    def __init__(self, value):
        self.value = value
        self.marked = False

    def mark(self):
        self.marked = True

    def is_marked(self):
        return self.marked

    def get_value(self):
        return self.value


class Board:
    def __init__(self, fields: list[list[Field]]):
        self.fields = fields
        self.won = False

    def mark_field(self, value):
        for row in self.fields:
            for field in row:
                if field.get_value() == value:
                    field.mark()
                    return

    def check(self):
        for row in self.fields:
            if all(field.is_marked() for field in row):
                self.won = True
                return True
        cols = zip(*self.fields)
        for col in cols:
            if all(field.is_marked() for field in col):
                self.won = True
                return True
        return False

    def is_winner(self):
        return self.won

    def get_unmarked_sum(self):
        return sum(sum([field.get_value() for field in row if not field.is_marked()]) for row in self.fields)


class Bingo:
    def __init__(self, numbers: list[int], boards: list[Board]):
        self.numbers = numbers
        self.boards = boards

    def game(self):
        c = 0
        for num in self.numbers:
            for board in self.boards:
                if board.is_winner():
                    continue
                board.mark_field(num)
                board.check()
                if board.is_winner():
                    c += 1
                    if c == len(self.boards):
                        return num * board.get_unmarked_sum()


def prepare_data(data: list[str]):
    numbers = [int(n) for n in data[0][:-1].split(',')]
    boards = []
    fields = []
    for line in data[2:]:
        if line == '\n':
            boards.append(Board(fields))
            fields = []
            continue
        row = [Field(int(n)) for n in line.split()]
        fields.append(row)
    boards.append(Board(fields))
    return numbers, boards


def get_winner(data):
    numbers, boards = prepare_data(data)
    bingo = Bingo(numbers, boards)
    return bingo.game()


if __name__ == '__main__':
    test_data = parser("input/day4_test")
    actual_data = parser("input/day4")

    print(get_winner(test_data))
    print(get_winner(actual_data))
