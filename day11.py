
def calc(x, y, serial):
    """
    Find the fuel cell's rack ID, which is its X coordinate plus 10.
    Begin with a power level of the rack ID times the Y coordinate.
    Increase the power level by the value of the grid serial number (your puzzle
    input).
    Set the power level to itself multiplied by the rack ID.
    Keep only the hundreds digit of the power level (so 12345 becomes 3; numbers
    with no hundreds digit become 0).
    Subtract 5 from the power level.
    """
    rackId = x + 10
    rackLvl = rackId * y
    temp = (rackLvl + serial) * rackId
    temp = temp // 100 - (temp // 1000 * 10)
    return temp - 5

def test1():
    assert calc(3, 5, 8) == 4
    assert calc(122,79,57) == -5
    assert calc(217,196,39) == 0
    assert calc(101,153,71) == 4

def makeGrid(n, serial):
    return [[calc(i, j, serial) for j in range(0, n)]
            for i in range(0, n)]

def calcN(grid, x, y, n):
    s = 0
    for i in range(x, x+n):
        for j in range(y, y+n):
            s += grid[i][j]
    return s

def _calcN(grid, x, y, n):
    s = 0
    for i in range(x, x+n-1):
        s += grid[i][y+n-1]
    for j in range(y, y+n):
        s += grid[x+n-1][j]
    return s

def makeSGrid(grid, n, cc):
    return [[calcN(grid, i, j, cc) for j in range(0, n-cc)]
            for i in range(0, n-cc)]

def solve(n, serial, cc):
    grid = makeGrid(n, serial)
    sgrid = makeSGrid(grid, n, cc)
    m = max(max(col) for col in sgrid)
    for i in range(0, n-cc):
        for j in range(0, n-cc):
            if sgrid[i][j] == m:
                return i, j
    return None

def _solve(grid, sgrid, n, cc):
    ss = None
    for i in range(0, n-cc):
        for j in range(0, n-cc):
            sgrid[i][j] += _calcN(grid, i, j, cc)
            m = sgrid[i][j]
            #m = calcN(grid, i, j, cc)
            if ss is None or m > ss[0]:
                ss = (m, i, j, cc)
    #print(cc, (n-cc)*(n-cc)*(cc*2-1), ss)
    return ss

def solve2(n, serial):
    grid = makeGrid(n, serial)
    sgrid = [[0 for j in range(0, n)] for i in range(0, n)]
    ss = None
    for cc in range(1, 300):
        res = _solve(grid, sgrid, n, cc)
        if ss is None:
            ss = res
        elif res[0] > ss[0]:
            ss = res
        elif res[0] < 0:
            break
    return ss

def test2():
    assert solve(300, 18, 3) == (33, 45)
    assert solve(300, 42, 3) == (21, 61)
    assert solve2(300, 18) == (113, 90, 269, 16)

def main():
    print('Part 1:', solve(300, 5791, 3))
    print('Part 2:', solve2(300, 5791)[1:])

if __name__ == '__main__':
    test1()
    test2()
    main()
