
dist = lambda a, b: sum(abs(x1-x2) for x1, x2 in zip(a, b))

def parse(text):
    arr = [int(t) for t in text.split(',')]
    return tuple(arr)

def solveR(data, chain, a):
    new = set()
    for b in data:
        if b not in chain and dist(a, b) <= 3:
            chain.add(b)
            new.add(b)
    for b in new:
        data.remove(b)
    for b in new:
        solveR(data, chain, b)

def solve(data):
    data = set(parse(t) for t in data)
    numChain = 0
    while data:
        a = data.pop()
        chain = set([a])
        solveR(data, chain, a)
        numChain += 1
    return numChain

def test1():
    data = [
        "0,0,0,0",
        "3,0,0,0",
        "0,3,0,0",
        "0,0,3,0",
        "0,0,0,3",
        "0,0,0,6",
        "9,0,0,0",
        "12,0,0,0",
    ]
    assert solve(data) == 2

def test2():
    data = [
        "-1,2,2,0",
        "0,0,2,-2",
        "0,0,0,-2",
        "-1,2,0,0",
        "-2,-2,-2,2",
        "3,0,2,-1",
        "-1,3,2,2",
        "-1,0,-1,0",
        "0,2,1,-2",
        "3,0,0,0",
    ]
    assert solve(data) == 4

def test3():
    data = [
        "1,-1,-1,-2",
        "-2,-2,0,1",
        "0,2,1,3",
        "-2,3,-2,1",
        "0,2,3,-2",
        "-1,-1,1,-2",
        "0,-2,-1,0",
        "-2,2,3,-1",
        "1,2,2,0",
        "-1,-2,0,-2",
    ]
    assert solve(data) == 8

def main():
    with open('day25.txt', 'r') as f:
        data = f.readlines()
    print('Part 1:', solve(data))

if __name__ == '__main__':
    test1()
    test2()
    test3()
    main()
