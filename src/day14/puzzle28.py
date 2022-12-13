from src.data_parser import parser


class Polymer:
    def __init__(self, template, pair_insertion_rules):
        self.polymer = template
        self.rules = pair_insertion_rules

    def process(self, steps):
        lets, pairs = self.get_lets_pairs()
        for _ in range(steps):
            pair_changes = {pair: 0 for pair in self.rules.keys()}
            for pair, num in pairs.items():
                if num == 0:
                    continue
                let = self.rules[pair]
                lets[let] += num
                pair_changes[pair] -= num
                new_pair1 = pair[0] + let
                new_pair2 = let + pair[1]
                pair_changes[new_pair1] += num
                pair_changes[new_pair2] += num
            for pair, num in pair_changes.items():
                if num == 0:
                    continue
                pairs[pair] += num
        return max(lets.values()), min(lets.values())

    def get_lets_pairs(self):
        lets = {let: self.polymer.count(let) for let in set(self.rules.values())}
        pairs = {pair: 0 for pair in self.rules.keys()}
        for i in range(len(self.polymer) - 1):
            pair = self.polymer[i:i + 2]
            pairs[pair] += 1
        return lets, pairs

    def quantity_subtraction(self, steps):
        mx, mn = self.process(steps)
        return mx - mn


def process_data(data):
    template = data[0].strip()
    rules = dict()
    for line in data[2:]:
        k, v = line.strip().split(' -> ')
        rules[k] = v
    return template, rules


def subtract_result(data, steps):
    template, rules = process_data(data)
    polymer = Polymer(template, rules)
    return polymer.quantity_subtraction(steps)


if __name__ == '__main__':
    test_data = parser("input/day14_test")
    actual_data = parser("input/day14")

    print(subtract_result(test_data, 40))
    print(subtract_result(actual_data, 40))

