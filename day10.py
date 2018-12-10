import re

parse_re = re.compile(
    r'(?P<name>\w+)=<\s*(?P<x>-?\d+)\s*,\s*(?P<y>-?\d+)\s*>')

class Dot:
    def __init__(self, pos, v):
        self.pos = pos
        self.v = v

    def tick(self):
        self.pos = (self.pos[0] + self.v[0], self.pos[1] + self.v[1])

def parse(text):
    p, v = parse_re.findall(text)
    p = (int(p[1]), int(p[2]))
    v = (int(v[1]), int(v[2]))
    return Dot(p, v)

def dprint(dots, i, limit=None):
    pos = list(map(lambda d: d.pos, dots))
    x_min = min(map(lambda d: d[0], pos))-1
    y_min = min(map(lambda d: d[1], pos))-1
    x_max = max(map(lambda d: d[0], pos))+1
    y_max = max(map(lambda d: d[1], pos))+1
    w = x_max - x_min
    h = y_max - y_min
    if limit and h > limit:
        return False
    print('Part 1:')
    for y in range(y_min, y_max):
        for x in range(x_min, x_max):
            dot = (x, y)
            if dot in pos:
                print('#', end='')
            else:
                print('.', end='')
        print()
    print('Part 2:', i)
    print()
    return True

def tick(dots, i):
    for dot in dots:
        dot.tick()
    dprint(dots, i)

def process(dots, n):
    for i in range(0, n):
        for dot in dots:
            dot.tick()
    dprint(dots, n)

def process2(dots):
    i = 1
    while True:
        for dot in dots:
            dot.tick()
        if dprint(dots, i, 20):
            break
        i += 1

def test1():
    data = """position=< 9,  1> velocity=< 0,  2>
    position=< 7,  0> velocity=<-1,  0>
    position=< 3, -2> velocity=<-1,  1>
    position=< 6, 10> velocity=<-2, -1>
    position=< 2, -4> velocity=< 2,  2>
    position=<-6, 10> velocity=< 2, -2>
    position=< 1,  8> velocity=< 1, -1>
    position=< 1,  7> velocity=< 1,  0>
    position=<-3, 11> velocity=< 1, -2>
    position=< 7,  6> velocity=<-1, -1>
    position=<-2,  3> velocity=< 1,  0>
    position=<-4,  3> velocity=< 2,  0>
    position=<10, -3> velocity=<-1,  1>
    position=< 5, 11> velocity=< 1, -2>
    position=< 4,  7> velocity=< 0, -1>
    position=< 8, -2> velocity=< 0,  1>
    position=<15,  0> velocity=<-2,  0>
    position=< 1,  6> velocity=< 1,  0>
    position=< 8,  9> velocity=< 0, -1>
    position=< 3,  3> velocity=<-1,  1>
    position=< 0,  5> velocity=< 0, -1>
    position=<-2,  2> velocity=< 2,  0>
    position=< 5, -2> velocity=< 1,  2>
    position=< 1,  4> velocity=< 2,  1>
    position=<-2,  7> velocity=< 2, -2>
    position=< 3,  6> velocity=<-1, -1>
    position=< 5,  0> velocity=< 1,  0>
    position=<-6,  0> velocity=< 2,  0>
    position=< 5,  9> velocity=< 1, -2>
    position=<14,  7> velocity=<-2,  0>
    position=<-3,  6> velocity=< 2, -1>"""
    data = data.split('\n')
    data = map(str.strip, data)
    data = map(parse, data)
    dots = list(data)
    process(dots, 3)

def main():
    with open('day10.txt', 'r') as f:
        data = f.readlines()
    data = map(str.strip, data)
    data = map(parse, data)
    dots = list(data)
    process2(dots)

if __name__ == '__main__':
    test1()
    main()
