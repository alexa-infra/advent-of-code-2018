from collections import defaultdict
import math
import heapq

def dist(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

TORCH, CLIMB, NOTHING = list(range(3))
equipment = [TORCH, CLIMB, NOTHING]

def equip(inType):
    if inType == 0:
        return CLIMB, TORCH
    if inType == 1:
        return CLIMB, NOTHING
    if inType == 2:
        return TORCH, NOTHING
    return None

def canMove(withEq, toType):
    return withEq in equip(toType)

def iterCoord(p):
    x, y = p
    yield x-1, y
    yield x, y-1
    yield x+1, y
    yield x, y+1

def iterCave(pos):
    for p in iterCoord(pos):
        if p[0] >= 0 and p[1] >= 0:
            yield p

def iterEq(t1):
    for eq in equipment:
        if canMove(eq, t1):
            yield eq

class State:
    def __init__(self, depth, target):
        self.depth = depth
        self.target = target
        self.mouth = (0, 0)
        self.mx = None
        self.my = None
        self.cache = {}

    def getType(self, p):
        return self.erosionLevel(p) % 3

    def erosionLevel(self, p):
        if p in self.cache:
            return self.cache[p]
        self.cache[p] = lvl = (self.geoIndex(p) + self.depth) % 20183
        return lvl

    def geoIndex(self, p):
        x, y = p
        if p == self.mouth:
            return 0
        if p == self.target:
            return 0
        if x == 0:
            return y * 48271
        if y == 0:
            return x * 16807
        return self.erosionLevel((x-1, y)) * self.erosionLevel((x, y-1))

    def getRisk(self):
        tx, ty = self.target
        risk = 0
        for y in range(0, ty+1):
            for x in range(0, tx+1):
                risk += self.getType((x, y))
        return risk

    def solve(self):
        """ A-star, a bit modified, without visited-set
            a node might be visited multiple time, if new distance_from_start
            is better than old.
        """
        start, goal = self.mouth + (TORCH,), self.target + (TORCH,)
        heuristic_cost_estimate = lambda x: dist((x[0], x[1]), self.mouth)
        distances_from_start = defaultdict(lambda: math.inf)
        distances_from_start[start] = 0
        frontier = [(heuristic_cost_estimate(start), start)]
        heapq.heapify(frontier)
        frontier_set = set([start])

        def get_neighbours(cave):
            x, y, eq = cave
            pos = (x, y)
            t1 = self.getType(pos)
            for p in iterCave(pos):
                t2 = self.getType(p)
                if canMove(eq, t1) and canMove(eq, t2):
                    yield p + (eq,), 1
            for eq1 in iterEq(t1):
                if eq1 != eq:
                    yield pos + (eq1,), 7

        while frontier:
            _, current = heapq.heappop(frontier)
            frontier_set.remove(current)
            if current == goal:
                return distances_from_start[goal]
            for neighbour, _dist in get_neighbours(current):
                distance_from_start = distances_from_start[current] + _dist
                if distance_from_start >= distances_from_start[neighbour]:
                    continue
                if neighbour not in frontier_set:
                    dd = distance_from_start + heuristic_cost_estimate(neighbour)
                    frontier_set.add(neighbour)
                    heapq.heappush(frontier, (dd, neighbour))
                distances_from_start[neighbour] = distance_from_start

    @classmethod
    def estimateRisk(cls, depth, target):
        s = cls(depth, target)
        return s.getRisk()

    @classmethod
    def estimateTime(cls, depth, target):
        s = cls(depth, target)
        return s.solve()

def test1():
    assert State.estimateRisk(510, (10, 10)) == 114

def test2():
    assert State.estimateTime(510, (10, 10)) == 45

def main():
    depth = 8787
    target = (10, 725)
    print('Part 1:', State.estimateRisk(depth, target))
    print('Part 2:', State.estimateTime(depth, target))

if __name__ == '__main__':
    test1()
    test2()
    main()
