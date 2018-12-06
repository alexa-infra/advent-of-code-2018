from collections import defaultdict

def distance(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x2 - x1) + abs(y2 - y1)

def findCloses(a, data):
    d = {b: distance(a, b) for b in data}
    a_min = min(d.items(), key=lambda x: x[1])
    if list(d.values()).count(a_min[1]) > 1:
        return None
    return a_min[0]

def findMax(a, data):
    d = {b: distance(a, b) for b in data}
    return sum(d.values())

getx = lambda x: x[0]
gety = lambda x: x[1]

def solve(data):
    x_min = getx(min(data, key=getx))
    y_min = gety(min(data, key=gety))
    x_max = getx(max(data, key=getx))
    y_max = gety(max(data, key=gety))
    width = x_max - x_min
    height = y_max - y_min
    conv = lambda a: (getx(a) - x_min, gety(a) - y_min)
    data = list(map(conv, data))
    m = list(list(findCloses((i, j), data) for j in range(0, height+1)) for i in range(0, width+1))
    inf = set()
    for i in range(0, width+1):
        inf.add(m[i][0])
        inf.add(m[i][height])
    for j in range(0, height+1):
        inf.add(m[0][j])
        inf.add(m[width][j])
    dd = defaultdict(int)
    #names = dict(zip(data, 'abcdefgh'))
    #names[None] = '.'
    for i in range(0, width+1):
        for j in range(0, height+1):
            a = m[i][j]
            #if (i, j) in data:
            #    print(names[a].upper(), end='')
            #else:
            #    print(names[a], end='')
            if a is None or a in inf:
                continue
            dd[a] += 1
        #print()
    return max(dd.values())

def solve2(data, n):
    x_min = getx(min(data, key=getx))
    y_min = gety(min(data, key=gety))
    x_max = getx(max(data, key=getx))
    y_max = gety(max(data, key=gety))
    width = x_max - x_min
    height = y_max - y_min
    conv = lambda a: (getx(a) - x_min, gety(a) - y_min)
    data = list(map(conv, data))
    m = list(list(findMax((i, j), data) for j in range(0, height+1)) for i in range(0, width+1))
    #names = dict(zip(data, 'abcdefgh'))
    cc = 0
    for i in range(0, width+1):
        for j in range(0, height+1):
            a = m[i][j]
            #if (i, j) in data:
            #    print(names[(i, j)].upper(), end='')
            #elif a < n:
            #    print('#', end='')
            #else:
            #    print('.', end='')
            if a < n:
                cc += 1
        #print()
    return cc

def test1():
    data = [
        (1, 1),
        (1, 6),
        (8, 3),
        (3, 4),
        (5, 5),
        (8, 9),
    ]
    assert solve(data) == 17

def test2():
    data = [
        (1, 1),
        (1, 6),
        (8, 3),
        (3, 4),
        (5, 5),
        (8, 9),
    ]
    assert solve2(data, 32) == 16

def main():
    with open('day6.txt', 'r') as f:
        data = f.readlines()
    def conv(it):
        arr = it.split(', ')
        return int(arr[0]), int(arr[1])
    data = list(map(conv, data))
    print('Part 1:', solve(data))
    print('Part 2:', solve2(data, 10000))

if __name__ == '__main__':
    test1()
    test2()
    main()
