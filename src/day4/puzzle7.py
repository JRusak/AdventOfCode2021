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

    def mark_field(self, value):
        for row in self.fields:
            for field in row:
                if field.get_value() == value:
                    field.mark()
                    return

    def is_winner(self):
        for row in self.fields:
            if all(field.is_marked() for field in row):
                return True
        cols = zip(*self.fields)
        for col in cols:
            if all(field.is_marked() for field in col):
                return True
        return False

    def get_unmarked_sum(self):
        return sum(sum([field.get_value() for field in row if not field.is_marked()]) for row in self.fields)


class Bingo:
    def __init__(self, numbers, boards):
        self.numbers = numbers
        self.boards = boards

    def game(self):
        for num in self.numbers:
            for board in self.boards:
                board.mark_field(num)
                if board.is_winner():
                    return board.get_unmarked_sum() * num


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
