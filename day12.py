import re

parse_initial_re = re.compile(
    r'initial state: ([\.#]+)')
parse_re = re.compile(
    r'(?P<pattern>[\.#]{5}) => (?P<result>[\.#])')

def parse_initial(text):
    return parse_initial_re.match(text).group(1)

def parse_rule(text):
    m = parse_re.match(text).groupdict()
    return m['pattern'], m['result'] == '#'

def parse(lines):
    initial = parse_initial(lines[0])
    initial = [p == '#' for p in initial]
    rules = [parse_rule(line) for line in lines[2:]]
    rules = {k: v for k, v in rules}
    return initial, rules

class Node:
    def __init__(self, pos, plant):
        self.pos = pos
        self.plant = plant

class State:
    def __init__(self, rules, initial):
        self.rules = rules
        self.pots = []
        for idx, plant in enumerate(initial):
            self.pots.append(Node(idx, plant))

    @property
    def withPlants(self):
        return list(filter(lambda p: p.plant, self.pots))

    @property
    def mostLeft(self):
        return self.withPlants[0]

    @property
    def mostRight(self):
        return self.withPlants[-1]

    def extendBorders(self):
        left = self.mostLeft
        left_idx = self.pots.index(left)
        for idx in range(left_idx, 4):
            pos = self.pots[0].pos - 1
            self.pots.insert(0, Node(pos, False))
        right = self.mostRight
        right_idx = len(self.pots) - self.pots.index(right) - 1
        for idx in range(right_idx, 4):
            pos = self.pots[-1].pos + 1
            self.pots.insert(len(self.pots), Node(pos, False))

    def getIter(self):
        for i in range(0, len(self.pots)-4):
            arr = self.pots[i:i+5]
            arr = map(lambda p: p.plant, arr)
            arr = map(lambda plant: '#' if plant else '.', arr)
            yield ''.join(arr), i+2

    def generation(self):
        self.extendBorders()
        newpots = dict()
        for arr, cur in self.getIter():
            if arr in self.rules:
                newpots[cur] = self.rules[arr]
        for pos, plant in newpots.items():
            self.pots[pos].plant = plant

    def print(self):
        for pot in self.pots:
            if pot.pos == 0:
                print('^', end='')
            print('#' if pot.plant else '.', end='')
        print(' ', self.count())

    def print_str(self):
        arr = ['#' if pot.plant else '.' for pot in self.pots]
        text = ''.join(arr)
        return text.strip('.')

    def count(self):
        return sum(map(lambda p: p.pos, self.withPlants))

    @classmethod
    def solve(cls, rules, initial, n):
        s = cls(rules, initial)
        #s.print()
        for i in range(0, n):
            s.generation()
            #s.print()
        return s.count()

    @classmethod
    def solve2(cls, rules, initial, n):
        s = cls(rules, initial)
        text = s.print_str()
        i = 1
        while True:
            s.generation()
            ntext = s.print_str()
            if text == ntext:
                break
            text = ntext
            i += 1
        diff = n - i
        ss = 0
        for pot in s.withPlants:
            ss += pot.pos + diff
        return ss

def test1():
    with open('day12-1.txt', 'r') as f:
        lines = f.readlines()
    initial, rules = parse(lines)
    assert State.solve(rules, initial, 20) == 325

def main():
    with open('day12.txt', 'r') as f:
        lines = f.readlines()
    initial, rules = parse(lines)
    print('Part 1:', State.solve(rules, initial, 20))
    print('Part 2:', State.solve2(rules, initial, 50000000000))

if __name__ == '__main__':
    test1()
    main()
