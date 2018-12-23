import re

parse_re = re.compile(
    r'pos\=\<(?P<x>-?\d+),(?P<y>-?\d+),(?P<z>-?\d+)\>, r\=(?P<r>\d+)'
)

def parse(text):
    m = parse_re.match(text)
    d = m.groupdict()
    pos = int(d['x']), int(d['y']), int(d['z'])
    r = int(d['r'])
    return pos, r

def dist(a, b):
    return sum(abs(x1-x2) for x1, x2 in zip(a, b))

def getinrange(data):
    mmax = max(data, key=lambda d: d[1])
    maxp, maxr = mmax
    pp = [(p, r) for p, r in data if dist(p, maxp) <= maxr]
    return len(pp)

def solve(data):
    pp = [p for p, r in data]
    xs = [x for x, y, z in pp]
    ys = [y for x, y, z in pp]
    zs = [z for x, y, z in pp]
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)
    zmin, zmax = min(zs), max(zs)
    dd = 1
    zero = (0, 0, 0)
    while dd < xmax - xmin:
        dd *= 2
    while True:
        tcount = 0
        best = None
        bestVal = None
        for x in range(xmin, xmax+1, dd):
            for y in range(ymin, ymax+1, dd):
                for z in range(zmin, zmax+1, dd):
                    pos = (x, y, z)
                    count = 0
                    for p, r in data:
                        if (dist(pos, p) - r) / dd <= 0:
                            count += 1
                    if count > tcount:
                        tcount = count
                        best = pos
                        bestVal = dist(best, zero)
                    elif count == tcount:
                        if best is None or dist(pos, zero) < bestVal:
                            best = pos
                            bestVal = dist(best, zero)
        if dd > 1:
            x, y, z = best
            xx = (x - dd, x + dd)
            yy = (y - dd, y + dd)
            zz = (z - dd, z + dd)
            xmin, xmax = min(xx), max(xx)
            ymin, ymax = min(yy), max(yy)
            zmin, zmax = min(zz), max(zz)
            dd = dd // 2
        else:
            return best, bestVal

def test1():
    data = [
        "pos=<0,0,0>, r=4",
        "pos=<1,0,0>, r=1",
        "pos=<4,0,0>, r=3",
        "pos=<0,2,0>, r=1",
        "pos=<0,5,0>, r=3",
        "pos=<0,0,3>, r=1",
        "pos=<1,1,1>, r=1",
        "pos=<1,1,2>, r=1",
        "pos=<1,3,1>, r=1",
    ]
    data = [parse(d) for d in data]
    assert getinrange(data) == 7

def test2():
    data = [
        "pos=<10,12,12>, r=2",
        "pos=<12,14,12>, r=2",
        "pos=<16,12,12>, r=4",
        "pos=<14,14,14>, r=6",
        "pos=<50,50,50>, r=200",
        "pos=<10,10,10>, r=5",
    ]
    data = [parse(d) for d in data]
    best, bestVal = solve(data)
    assert bestVal == 36

def main():
    with open('day23.txt', 'r') as f:
        data = f.readlines()
    data = [parse(d) for d in data]
    print('Part 1:', getinrange(data))
    best, bestVal = solve(data)
    print('Part 2:', bestVal)

if __name__ == '__main__':
    test1()
    test2()
    main()
