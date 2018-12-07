import re

parse_re = re.compile(
    r'Step (?P<node1>\w) must be finished before step (?P<node2>\w) can begin.')

def parse(text):
    m = parse_re.match(text)
    d = m.groupdict()
    return d['node1'], d['node2']

class Node:
    def __init__(self, name):
        self.name = name
        self.parents = []
        self.children = []

def buildTree(data):
    nodesByName = {}

    def link(a, b):
        node_a = getNode(a)
        node_b = getNode(b)
        node_b.parents.append(node_a)
        node_a.children.append(node_b)

    def getNode(name):
        if name in nodesByName:
            return nodesByName[name]
        node = Node(name)
        nodesByName[name] = node
        return node

    for a, b in data:
        link(a, b)

    roots = filter(lambda x: len(x.parents) == 0, nodesByName.values())
    return list(roots)

def solve(data):
    nodes = buildTree(data)
    res = ''
    while nodes:
        nodes.sort(key=lambda x: x.name)
        node = nodes.pop(0)
        assert not node.parents
        for child in node.children:
            child.parents.remove(node)
            if not child.parents:
                nodes.append(child)
        res += node.name
    return res

def solve2(data, n, c):
    nodes = buildTree(data)
    nodes.sort(key=lambda x: x.name)
    workers = [(None, 0) for i in range(0, n)]
    time = 0
    while True:
        for idx, worker in enumerate(workers):
            node, counter = worker
            if counter > 0:
                counter -= 1
                workers[idx] = (node, counter)
                if counter > 0:
                    continue
            if node:
                for child in node.children:
                    child.parents.remove(node)
                    if not child.parents:
                        nodes.append(child)
                        nodes.sort(key=lambda x: x.name)
                workers[idx] = (None, 0)
            if nodes:
                node = nodes.pop(0)
                counter = c + ord(node.name) - 64
                workers[idx] = (node, counter)
        free_workers = all(map(lambda x: x[1] == 0, workers))
        if free_workers:
            break
        time += 1
    return time

def test1():
    data = [
        "Step C must be finished before step A can begin.",
        "Step C must be finished before step F can begin.",
        "Step A must be finished before step B can begin.",
        "Step A must be finished before step D can begin.",
        "Step B must be finished before step E can begin.",
        "Step D must be finished before step E can begin.",
        "Step F must be finished before step E can begin.",
    ]
    data = list(map(parse, data))
    assert solve(data) == 'CABDFE'
    assert solve2(data, 2, 0) == 15

def main():
    with open('day7.txt', 'r') as f:
        data = f.readlines()
    data = list(map(parse, data))
    print('Part 1:', solve(data))
    print('Part 2:', solve2(data, 5, 60))

if __name__ == '__main__':
    test1()
    main()
