from src.data_parser import parser

LETS_TO_NUMS = {'ABCEFG': 0, 'CF': 1, 'ACDEG': 2, 'ACDFG': 3, 'BCDF': 4,
                'ABDFG': 5, 'ABDEFG': 6, 'ACF': 7, 'ABCDEFG': 8, 'ABCDFG': 9}


def process_example_data(data):
    a, b = [], []
    for idx, line in enumerate(data):
        if idx & 1:
            b.append(line.strip().split())
        else:
            a.append(line[:-3].split())
    return zip(a, b)


def process_data(data):
    data = [(n.strip().split() for n in d.split('|')) for d in data]
    return data


def get_initial_dict(numbers: list[str]):
    h = {2: 'CF', 3: 'A', 4: 'BD'}
    d = {}
    num = numbers[0]
    val = h[len(num)]

    d[num] = val
    for n in numbers[1:]:
        n = set(n)
        lets = h[len(n)]
        n = ''.join(n.difference(set(num)))
        d[n] = lets
    return d


def update_dict(d: dict, key: str, val: str):
    for k in d.keys():
        if key in k:
            v = d.pop(k)
            d[k.replace(key, '')] = v.replace(val, '')
            break
    d[key] = val


def check_coded_number(d, num: set[str]):
    output = ''
    for k, v in d.items():
        k = set(k)
        if k.issubset(num):
            num = num.difference(k)
            output += v
    return ''.join(num), output


def get_missing_letter(out):
    out = set(out)
    for k in LETS_TO_NUMS.keys():
        k = set(k)
        if out.issubset(k) and len(k) - len(out) == 1:
            return k.difference(out).pop()


def code(coded_numbers: list[str]):
    coded_numbers.sort(key=lambda x: len(x))
    d = get_initial_dict(coded_numbers[:3])
    coded_numbers = coded_numbers[3:-1]

    while len(d) != 7:
        nums_to_rm = []
        for num in coded_numbers:
            sv = num
            num = set(num)
            n, out = check_coded_number(d, num)

            if len(n) != 1:
                continue
            nums_to_rm.append(sv)
            val = get_missing_letter(out)
            update_dict(d, n, val)
        for num in nums_to_rm:
            coded_numbers.remove(num)
    return d


def get_number(data):
    coded_numbers, result = data
    d = code(coded_numbers)
    nums = ''
    for coded_res in result:
        lets = set()
        for let in coded_res:
            lets.add(d[let])
        for k, v in LETS_TO_NUMS.items():
            k = set(k)
            if lets == k:
                nums += str(v)
    return int(nums)


def count_numbers(data):
    return sum(get_number(pair) for pair in data)


if __name__ == '__main__':
    test_data = parser("input/day8_test")
    actual_data = parser("input/day8")

    new_test_data = process_example_data(test_data)
    new_actual_data = process_data(actual_data)

    print(count_numbers(new_test_data))
    print(count_numbers(new_actual_data))
