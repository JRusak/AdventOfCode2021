from src.data_parser import parser
from collections import deque


class Polymer:
    def __init__(self, template, pair_insertion_rules):
        self.polymer = template
        self.rules = pair_insertion_rules

    def process_step(self):
        new_lets = deque()
        for i in range(len(self.polymer) - 1):
            pair = self.polymer[i:i + 2]
            new_let = self.rules[pair]
            new_lets.append(new_let)

        new_polymer = self.polymer[0]
        for let in self.polymer[1:]:
            new_polymer += new_lets.popleft()
            new_polymer += let
        self.polymer = new_polymer

    def process(self, steps):
        for _ in range(steps):
            self.process_step()

    def quantity_subtraction(self):
        lets = set(self.polymer)
        quantity_list = []
        for let in lets:
            quantity = self.polymer.count(let)
            quantity_list.append(quantity)
        return max(quantity_list) - min(quantity_list)


def process_data(data):
    template = data[0].strip()
    rules = dict()
    for line in data[2:]:
        k, v = line.strip().split(' -> ')
        rules[k] = v
    return template, rules


def subtract_result(data):
    template, rules = process_data(data)
    polymer = Polymer(template, rules)
    polymer.process(10)
    return polymer.quantity_subtraction()


if __name__ == '__main__':
    test_data = parser("input/day14_test")
    actual_data = parser("input/day14")

    print(subtract_result(test_data))
    print(subtract_result(actual_data))

