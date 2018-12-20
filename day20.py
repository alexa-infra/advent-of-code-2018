from collections import defaultdict

# NESW

has_north = lambda r: bool(r & 1)
has_east = lambda r: bool(r & 2)
has_south = lambda r: bool(r & 4)
has_west = lambda r: bool(r & 8)

set_north = lambda src, target: (src | 1, target | 4)
set_east = lambda src, target: (src | 2, target | 8)
set_south = lambda src, target: (src | 4, target | 1)
set_west = lambda src, target: (src | 8, target | 2)

def add(m, p, ch):
    x, y = p
    a = m[p]
    if ch == 'N':
        p1 = (x, y - 1)
        if has_north(a):
            return p1
        b = m[p1]
        a, b = set_north(a, b)
    elif ch == 'E':
        p1 = (x + 1, y)
        if has_east(a):
            return p1
        b = m[p1]
        a, b = set_east(a, b)
    elif ch == 'S':
        p1 = (x, y + 1)
        if has_south(a):
            return p1
        b = m[p1]
        a, b = set_south(a, b)
    elif ch == 'W':
        p1 = (x - 1, y)
        if has_west(a):
            return p1
        b = m[p1]
        a, b = set_west(a, b)
    m[p] = a
    m[p1] = b
    return p1

def find_end_bracket(text, start):
    counter = 0
    for pos in range(start, len(text)):
        ch = text[pos]
        if ch == '(':
            counter += 1
        elif ch == ')':
            counter -= 1
            if counter == 0:
                return pos
    return None

class Sequence:
    def __init__(self, items):
        self.nodes = items

    def __repr__(self):
        return 'Sequence: {}'.format(self.nodes)

def parse(text):
    start = 0
    parts = []
    pos = 0
    while pos < len(text):
        ch = text[pos]
        if ch == '(':
            if start != pos:
                part = text[start:pos]
                parts.append(part)
            start = pos + 1
            pos = find_end_bracket(text, pos)
            part = text[start:pos]
            branches = parse_branch(part)
            parts.append(branches)
            start = pos + 1
        pos += 1
    if start != pos:
        part = text[start:pos]
        parts.append(part)
    return Sequence(parts)

class Branch:
    def __init__(self, items):
        self.nodes = items

    def __repr__(self):
        return 'Branch: {}'.format(self.nodes)

def parse_branch(text):
    pos = 0
    branches = []
    start = 0
    while pos < len(text):
        ch = text[pos]
        if ch == '(':
            pos = find_end_bracket(text, pos)
        elif ch == '|':
            branch = text[start:pos]
            if '(' in branch:
                branch = parse(branch)
            branches.append(branch)
            start = pos + 1
        pos += 1
    branch = text[start:pos]
    if '(' in branch:
        branch = parse(branch)
    branches.append(branch)
    return Branch(branches)

def walk_r(maze, endpoints, data, level=0):
    if isinstance(data, Sequence):
        for node in data.nodes:
            endpoints = walk_r(maze, endpoints, node, level + 1)
        return endpoints
    if isinstance(data, Branch):
        new_endpoints = set()
        for node in data.nodes:
            for ep in walk_r(maze, endpoints, node, level + 1):
                new_endpoints.add(ep)
        return new_endpoints
    if isinstance(data, str):
        new_endpoints = set()
        for p in endpoints:
            for ch in data:
                p = add(maze, p, ch)
            new_endpoints.add(p)
        return new_endpoints
    return None

def start_walk(text):
    data = parse(text)
    start = (0, 0)
    maze = defaultdict(int)
    walk_r(maze, set([start]), data)
    return maze

def print_lab(m, vis):
    coords = list(m.keys())
    xmin = min(x for x, y in coords)
    xmax = max(x for x, y in coords)
    ymin = min(y for x, y in coords)
    ymax = max(y for x, y in coords)
    for y in range(ymin, ymax+1):
        for x in range(xmin, xmax+1):
            p = (x, y)
            if p in vis:
                print('X', end='')
            elif p in m:
                print('#', end='')
            else:
                print('.', end='')
        print()
    print()

def iterRoom(m, p):
    x, y = p
    v = m[p]
    if has_north(v):
        yield x, y - 1
    if has_east(v):
        yield x + 1, y
    if has_south(v):
        yield x, y + 1
    if has_west(v):
        yield x - 1, y

def solve(text):
    maze = start_walk(text)
    node = (0, 0)
    visited = {}
    visited[node] = 0
    next_nodes = [node]
    while next_nodes:
        p = next_nodes.pop()
        index = visited[p] + 1
        for p1 in iterRoom(maze, p):
            if p1 not in visited:
                visited[p1] = index
                next_nodes.append(p1)
        #print_lab(maze, visited)
    at_least1k = len(list(filter(lambda x: x >= 1000, visited.values())))
    max_path = max(visited.values())
    return max_path, at_least1k

def test1():
    text = '^WNE$'
    text = text[1:-1]
    assert solve(text) == (3, 0)

def test2():
    text = '^ENWWW(NEEE|SSE(EE|N))$'
    text = text[1:-1]
    assert solve(text) == (10, 0)

def test3():
    text = '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$'
    text = text[1:-1]
    assert solve(text) == (18, 0)

def main():
    with open('day20.txt', 'r') as f:
        text = f.read().strip()
        text = text[1:-1]
    max_path, at_least1k = solve(text)
    print('Part 1:', max_path)
    print('Part 2:', at_least1k)

if __name__ == '__main__':
    test1()
    test2()
    test3()
    main()
