import re
from collections import defaultdict

parse_re = re.compile(
    r'^#(?P<name>\d+) @ (?P<x>\d+),(?P<y>\d+): (?P<w>\d+)x(?P<h>\d+)$')

def parse(text):
    match = parse_re.match(text)
    d = match.groupdict()
    return d['name'], int(d['x']), int(d['y']), int(d['w']), int(d['h'])

def solve(data):
    idata = map(parse, data)
    arr = set()
    same = set()
    for _, x, y, w, h in idata:
        for xc in range(x, x + w):
            for yc in range(y, y + h):
                cc = (xc, yc)
                if cc in arr:
                    same.add(cc)
                else:
                    arr.add(cc)
    return len(same)

def solve2(data):
    idata = list(map(parse, data))
    d = defaultdict(int)
    for name, x, y, w, h in idata:
        for xc in range(x, x + w):
            for yc in range(y, y + h):
                cc = (xc, yc)
                d[cc] += 1
    for name, x, y, w, h in idata:
        good = True
        for xc in range(x, x + w):
            for yc in range(y, y + h):
                cc = (xc, yc)
                if d[cc] > 1:
                    good = False
        if good:
            return name
    return None

def test1():
    data = [
        '#1 @ 1,3: 4x4',
        '#2 @ 3,1: 4x4',
        '#3 @ 5,5: 2x2',
    ]
    assert solve(data) == 4

def test2():
    data = [
        '#1 @ 1,3: 4x4',
        '#2 @ 3,1: 4x4',
        '#3 @ 5,5: 2x2',
    ]
    assert solve2(data) == '3'

def main():
    with open('day3.txt', 'r') as f:
        data = f.readlines()
    print('Part 1:', solve(data))
    print('Part 2:', solve2(data))

if __name__ == '__main__':
    test1()
    test2()
    main()
