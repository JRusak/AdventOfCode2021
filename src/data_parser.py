def parser(filename):
    output = []
    with open(filename, 'r') as fh:
        for line in fh:
            output.append(line)
    return output
