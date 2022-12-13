import heapq

from src.data_parser import parser


class Node:
    def __init__(self, position, cost):
        self.start = False
        self.end = False
        self._position = position
        self._cost = cost
        self._adjacents = []
        self._visited = False
        self._previous = None
        self._visible = False

    def add_adjacent(self, adjacent_node):
        self._adjacents.append(adjacent_node)
        # self._adjacents.sort(key=lambda node: node.get_cost())

    def get_cost(self):
        return self._cost

    def get_adjacents(self):
        # self._adjacents.sort(key=lambda node: node.get_cost())
        return self._adjacents

    def get_position(self):
        return self._position

    def set_visited(self):
        self._visited = True

    def is_visited(self):
        return self._visited

    def set_visible(self):
        self._visible = True

    def is_visible(self):
        return self._visible

    def set_previous(self, other_node):
        self._previous = other_node

    def get_previous(self):
        return self._previous


class NodeCreator:
    def __init__(self, data):
        self.data = data
        self.nodes = self.get_nodes()[0]

    def get_nodes(self, in_tuples=0):
        table = self.make_table(self.data)
        nodes = self.create_nodes(table)
        self.add_adjacents(nodes)
        out_nodes = []
        for sub_nodes in nodes:
            for node in sub_nodes:
                if in_tuples:
                    out_nodes.append((node, node.get_cost))
                else:
                    out_nodes.append(node)
        return out_nodes, len(nodes[0])

    def create_nodes(self, table):
        nodes = []
        for i in range(len(table)):
            sub_nodes = []
            for j in range(len(table[i])):
                new_node = Node((i, j), int(table[i][j]))
                sub_nodes.append(new_node)
            nodes.append(sub_nodes)
        nodes[0][0].start = True
        nodes[-1][-1].end = True
        return nodes

    def make_table(self, data):
        return [list(i.strip()) for i in data]

    def add_adjacents(self, nodes):
        for i in range(len(nodes)):
            for j in range(len(nodes[i])):
                node = nodes[i][j]
                if j != 0:
                    node.add_adjacent(nodes[i][j-1])
                if j != len(nodes[i])-1:
                    node.add_adjacent(nodes[i][j+1])
                if i != 0:
                    node.add_adjacent(nodes[i-1][j])
                if i != len(nodes)-1:
                    node.add_adjacent(nodes[i+1][j])


class PathFinder:
    def __init__(self, nodes):
        self.nodes = nodes
        self.start, self.end, self.costs = self.get_end_points_and_costs()

    def heuristic(self, current_node: Node):
        x1, y1 = current_node.get_position()
        x2, y2 = self.end.get_position()
        return abs(x1 - x2) + abs(y1 - y2)

    def print_nodes(self, width):
        text = ''
        for i, node in enumerate(self.nodes):
            if node.is_visible() and node.is_visited():
                text += str(node.get_cost())
            elif node.is_visited():
                text += '*'
            else:
                text += ' '
            if i % width == width - 1:
                text += '\n'
        return text[:len(text) - 1]

    def get_end_points_and_costs(self):
        start = None
        end = None
        costs = {}
        for node in self.nodes:
            costs[node] = float("inf")
            if node.start:
                start = node
            elif node.end:
                end = node
        return start, end, costs

    def a_star(self):
        start, end, costs = self.start, self.end, self.costs
        entry_number = 0
        nodes_queue = [(0, entry_number, start)]
        costs[start] = 0
        entry_number += 1
        f_costs = costs.copy()
        while nodes_queue:
            c_fcost, xxx, node = heapq.heappop(nodes_queue)
            node.set_visited()
            if node == end:
                break
            for neighbor in node.get_adjacents():
                n_cost = costs[node] + neighbor.get_cost()
                if neighbor not in costs or n_cost < costs[neighbor]:
                    costs[neighbor] = n_cost
                    f_costs[neighbor] = n_cost + self.heuristic(neighbor)
                    neighbor.set_previous(node)
                    heapq.heappush(nodes_queue, (f_costs[neighbor], entry_number, neighbor))
                    entry_number += 1

    def get_path_cost(self):
        temp = self.end
        cost = 0
        while temp != self.start:
            cost += temp.get_cost()
            prev = temp.get_previous()
            temp = prev
        return cost


def process_data(data):
    return NodeCreator(data).nodes


def path_counter(data):
    nodes = process_data(data)
    pf = PathFinder(nodes)
    pf.a_star()
    return pf.get_path_cost()


if __name__ == '__main__':
    test_data = parser("input/day15_test")
    actual_data = parser("input/day15")

    print(path_counter(test_data))
    print(path_counter(actual_data))
