from itertools import islice

def getNext(arr, n):
    return n % len(arr)

def getNumber(arr, start, length):
    it = islice(arr, start, start+length)
    return ''.join(map(str, it))

def tick(arr, elf1, elf2):
    a, b = arr[elf1], arr[elf2]
    s = a + b
    if s >= 10:
        x = s // 10
        y = s % 10
        arr.append(x)
        arr.append(y)
    else:
        arr.append(s)
    return getNext(arr, elf1 + a + 1), getNext(arr, elf2 + b + 1)

def print_arr(arr, elf1, elf2):
    for idx, ch in enumerate(arr):
        if idx == elf1:
            print('({})'.format(ch), end=' ')
        elif idx == elf2:
            print('[{}]'.format(ch), end=' ')
        else:
            print(ch, end=' ')
    print()

def solve(n):
    arr = [3, 7]
    elf1, elf2 = 0, 1
    #print_arr(arr, elf1, elf2)
    while len(arr) < n + 10:
        elf1, elf2 = tick(arr, elf1, elf2)
        #print_arr(arr, elf1, elf2)
    return getNumber(arr, n, 10)

def index_of(arr, *args):
    try:
        return arr.index(*args)
    except ValueError:
        return -1

def tester(arr, sub, lastIdx):
    idx = index_of(arr, sub[0], lastIdx)
    while idx != -1:
        found = True
        for i, n in enumerate(sub):
            if idx + i >= len(arr):
                return False, idx
            if arr[idx + i] != n:
                found = False
                break
        if found:
            return True, idx
        lastIdx = idx
        idx = index_of(arr, sub[0], idx + 1)
    return False, lastIdx

def solve2(txt):
    arr = [3, 7]
    elf1, elf2 = 0, 1
    tt = list(map(int, list(txt)))
    lastIdx = 0
    #print_arr(arr, elf1, elf2)
    nextTest = 10000
    while True:
        elf1, elf2 = tick(arr, elf1, elf2)
        #print_arr(arr, elf1, elf2)
        if len(arr) >= nextTest:
            found, lastIdx = tester(arr, tt, lastIdx)
            if found:
                break
            nextTest += 10000
    return lastIdx

def test1():
    assert solve(9) == '5158916779'
    assert solve(2018) == '5941429882'

def test2():
    assert solve2('51589') == 9
    assert solve2('59414') == 2018

def main():
    print('Part 1:', solve(209231))
    print('Part 2:', solve2('209231'))

if __name__ == '__main__':
    test1()
    test2()
    main()
