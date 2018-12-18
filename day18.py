
mapp = []
mapp2 = []
xmax = 0
ymax = 0

def iter9(x, y):
    for j in range(-1, 2):
        for i in range(-1, 2):
            if i == 0 and j == 0:
                continue
            yield x+i, y+j

def iterAdj(x, y):
    for a, b in iter9(x, y):
        if a < 0 or b < 0:
            continue
        if a >= xmax or b >= ymax:
            continue
        yield mapp[b][a]

def countAdj(x, y):
    a, b, c = 0, 0, 0
    for it in iterAdj(x, y):
        if it == '|':
            a += 1
        if it == '#':
            b += 1
        if it == '.':
            c += 1
    return a, b, c

def mutateTile(x, y):
    tile = mapp[y][x]
    a, b, c = countAdj(x, y)
    if tile == '.' and a >= 3:
        return '|'
    if tile == '|' and b >= 3:
        return '#'
    if tile == '#' and (b < 1 or a < 1):
        return '.'
    return tile

def mutateMap():
    global mapp, mapp2
    for y in range(0, ymax):
        for x in range(0, xmax):
            mapp2[y][x] = mutateTile(x, y)
    mapp, mapp2 = mapp2, mapp

def diffMap():
    diff = 0
    for y in range(0, ymax):
        for x in range(0, xmax):
            if mapp2[y][x] != mapp[y][x]:
                diff += 1
    return diff

def initMap(lines):
    global mapp, mapp2, xmax, ymax
    ymax = len(lines)
    xmax = len(lines[0])
    mapp = []
    mapp2 = []
    for line in lines:
        mapp.append(list(line))
        mapp2.append(list(line))

def printMap():
    for y in range(0, ymax):
        for x in range(0, xmax):
            print(mapp[y][x], end='')
        print()
    print()

def countMap():
    a, b, c = 0, 0, 0
    for y in range(0, ymax):
        for x in range(0, xmax):
            it = mapp[y][x]
            if it == '|':
                a += 1
            if it == '#':
                b += 1
            if it == '.':
                c += 1
    return a, b, c

def test1():
    with open('day18-1.txt', 'r') as f:
        data = f.readlines()
    initMap(data)
    #printMap()
    for i in range(0, 10):
        mutateMap()
        #printMap()
    a, b, c = countMap()
    assert a * b == 1147

def listRIndex(alist, value):
    return len(alist) - alist[-1::-1].index(value) - 1

def main():
    with open('day18.txt', 'r') as f:
        data = f.readlines()
    initMap(data)
    for i in range(0, 10):
        mutateMap()
    a, b, c = countMap()
    print('Part 1:', a * b)

    cycle = list()
    cycleStart = None
    initMap(data)
    for i in range(0, 800):
        mutateMap()
        s = countMap()
        if s in cycle:
            if cycleStart:
                cycleNext = listRIndex(cycle, s)
                if cycleNext == cycleStart + 1:
                    break
                else:
                    cycleStart = cycleNext
            else:
                cycleStart = listRIndex(cycle, s)
        elif cycleStart:
            cycleStart = None
        cycle.append(s)
    cycle = cycle[cycleStart:-1]
    n = 1000000000
    idx = (n - 1 - cycleStart) % len(cycle)
    a, b, c = cycle[idx]
    print('Part 2:', a * b)


if __name__ == '__main__':
    test1()
    main()
