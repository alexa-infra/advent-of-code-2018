import string

def process(text, remove=None):
    atext = list(text)
    idx = 0
    removeUp = remove.upper() if remove else None
    while idx + 1 < len(atext):
        a, b = atext[idx], atext[idx+1]
        if remove and a in (remove, removeUp):
            atext.pop(idx)
            idx = max(0, idx-1)
            continue
        if abs(ord(a) - ord(b)) == 32:
            atext.pop(idx)
            atext.pop(idx)
            idx = max(0, idx-1)
        else:
            idx += 1
    return ''.join(atext)

def solve1(text):
    s = process(text)
    return len(s)

def solve2(text):
    m = len(text)
    mch = None
    for ch in string.ascii_lowercase:
        s = process(text, ch)
        if len(s) < m:
            m = len(s)
            mch = ch
    return m, mch

def test1():
    assert process('dabAcCaCBAcCcaDA') == 'dabCBAcaDA'

def test2():
    assert process('aa') == 'aa'
    assert process('aA') == ''
    assert process('bbaA') == 'bb'
    assert process('aAbb') == 'bb'
    assert process('aAbbAa') == 'bb'
    assert process('aAaAaAb') == 'b'
    assert process('AAA') == 'AAA'
    assert process('ACacACacACacACacACacACacACacACacACac') == 'ACacACacACacACacACacACacACacACacACac'

def test3():
    assert solve2('dabAcCaCBAcCcaDA') == (4, 'c')

def main():
    with open('day5.txt', 'r') as f:
        data = f.read().strip()
    print('Part 1:', solve1(data))
    print('Part 2:', solve2(data))

if __name__ == '__main__':
    test1()
    test2()
    test3()
    main()
