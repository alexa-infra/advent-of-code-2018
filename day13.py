from copy import deepcopy

def move(x, y, direction):
    if direction == '^':
        return x, y - 1
    if direction == '>':
        return x + 1, y
    if direction == '<':
        return x - 1, y
    if direction == 'v':
        return x, y + 1
    return None

slash_corner = {
    '^': '>',
    '<': 'v',
    'v': '<',
    '>': '^',
}

backslash_corner = {
    '^': '<',
    '<': '^',
    'v': '>',
    '>': 'v',
}

def corner(el, direction):
    if el == '/':
        return slash_corner[direction]
    if el == '\\':
        return backslash_corner[direction]
    return None

crosses = {
    '^': '<^>',
    '>': '^>v',
    'v': '>v<',
    '<': 'v<^',
}

def cross(direction, counter):
    return crosses[direction][counter]

class Car:
    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = direction
        self.tempEl = None
        if direction in '<>':
            self.tempEl = '-'
        elif direction in 'v^':
            self.tempEl = '|'
        self.crash = None
        self.dirCounter = 0

    @property
    def nextPos(self):
        x, y = self.pos
        return move(x, y, self.direction)

    def move(self, track):
        x1, y1 = self.pos
        x, y = self.nextPos
        track[y1][x1] = self.tempEl
        self.tempEl = el = track[y][x]
        if el in '<^>v':
            newEl = 'X'
            self.crash = True
        elif el in '|-':
            newEl = self.direction
        elif el in '/\\':
            newEl = self.direction = corner(el, self.direction)
        elif el == '+':
            newEl = self.direction = cross(self.direction, self.dirCounter)
            self.dirCounter = (self.dirCounter + 1) % 3
        else:
            print('Element:', el, '!')
            print(self.direction)
            print(x1, y1)
            print(x, y)
            assert False
        track[y][x] = newEl
        self.pos = (x, y)

class Solver:
    def __init__(self, data):
        self.data = deepcopy(data)
        self.cars = []
        for y, line in enumerate(data):
            for x, ch in enumerate(line):
                if ch in '<^>v':
                    pos = (x, y)
                    self.cars.append(Car(pos, ch))

    def tick(self):
        self.cars.sort(key=lambda car: car.pos)
        for car in self.cars:
            car.move(self.data)
            if car.crash:
                return car.pos
        return None

    def tick2(self):
        self.cars.sort(key=lambda car: car.pos)
        for car in self.cars:
            if car.crash:
                continue
            car.move(self.data)
            if car.crash:
                pos = car.pos
                func = lambda c: not c.crash and c.pos == pos
                crashed = filter(func, self.cars)
                for car2 in crashed:
                    car2.crash = True
                    x, y = pos
                    self.data[y][x] = car2.tempEl

    @property
    def readyCars(self):
        func = lambda car: not car.crash
        return list(filter(func, self.cars))

    def print(self):
        for line in self.data:
            for ch in line:
                print(ch, end='')
            print()
        print()

    @classmethod
    def run(cls, data):
        s = Solver(data)
        #s.print()
        while True:
            res = s.tick()
            #s.print()
            if res is not None:
                return res

    @classmethod
    def run2(cls, data):
        s = Solver(data)
        #s.print()
        while True:
            s.tick2()
            #s.print()
            if len(s.readyCars) == 1:
                break
        car = s.readyCars[0]
        return car.pos

def test1():
    with open('day13-1.txt', 'r') as f:
        data = f.readlines()
    data = list(map(list, data))
    assert Solver.run(data) == (7, 3)

def main():
    with open('day13.txt', 'r') as f:
        data = f.readlines()
    data = [list(line) for line in data]
    print('Part 1:', Solver.run(data))
    print('Part 2:', Solver.run2(data))

if __name__ == '__main__':
    test1()
    main()
