from itertools import cycle

def solve(idata):
    cur = 0
    seen = set([cur])
    for it in cycle(idata):
        cur += it
        if cur in seen:
            break
        seen.add(cur)
    return cur

def main():
    with open('day1.txt', 'r') as f:
        data = f.readlines()
    idata = list(map(int, data))
    print('Part 1', sum(idata))
    print('Part 2', solve(idata))

def test1():
    text = '+1, -1'
    data = text.split(', ')
    idata = list(map(int, data))
    assert solve(idata) == 0

def test2():
    text = '+3, +3, +4, -2, -4'
    data = text.split(', ')
    idata = list(map(int, data))
    assert solve(idata) == 10

def test3():
    text = '-6, +3, +8, +5, -6'
    data = text.split(', ')
    idata = list(map(int, data))
    assert solve(idata) == 5

def test4():
    text = '+7, +7, -2, -7, -4'
    data = text.split(', ')
    idata = list(map(int, data))
    assert solve(idata) == 14

if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
    main()
