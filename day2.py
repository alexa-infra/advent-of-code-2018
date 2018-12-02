from itertools import combinations
from collections import defaultdict

def scan(text):
    d = defaultdict(int)
    for ch in text:
        d[ch] += 1
    uniq = set(d.values())
    if 2 in uniq and 3 in uniq:
        return 1
    if 2 in uniq:
        return 2
    if 3 in uniq:
        return 3
    return 0

def solve(items):
    items = list(map(scan, items))
    count2 = items.count(2) + items.count(1)
    count3 = items.count(3) + items.count(1)
    return count2 * count3

def isClose(a, b):
    if a == b:
        return False
    cc = 1
    it = zip(a, b)
    while cc >= 0:
        item = next(it, None)
        if item is None:
            return True
        ch1, ch2 = item
        if ch1 != ch2:
            cc -= 1
    return False

def getCommon(a, b):
    ret = list()
    for ch1, ch2 in zip(a, b):
        if ch1 == ch2:
            ret.append(ch1)
    return ''.join(ret)

def findClose(items):
    for a, b in combinations(items, 2):
        if isClose(a, b):
            return getCommon(a, b)
    return None

def main():
    with open('day2.txt', 'r') as f:
        items = f.readlines()
    print('Part 1:', solve(items))
    print('Part 2:', findClose(items))

def test1():
    data = 'abcdef,bababc,abbcde,abcccd,aabcdd,abcdee,ababab'
    words = data.split(',')
    assert solve(words) == 12

def test2():
    a, b = 'abcde', 'axcye'
    assert isClose(a, b) is False

def test3():
    a, b = 'abcde', 'abcfe'
    assert isClose(a, b) is True

def test4():
    a, b = 'xbcde', 'abcde'
    assert isClose(a, b) is True

def test5():
    a, b = 'xbcze', 'abcde'
    assert isClose(a, b) is False

def test6():
    a, b = 'xbcde', 'abcde'
    assert getCommon(a, b) == 'bcde'

if __name__ == '__main__':
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    main()
