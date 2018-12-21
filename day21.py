from day19 import runner, parse

def program(r0, ip, codes):
    """ Simple run of the code, the second part takes an eternity to reach """
    r = [r0, 0, 0, 0, 0, 0]
    s = set()
    m = None
    while r[ip] >= 0 and r[ip] < len(codes):
        code = codes[r[ip]]
        if r[ip] == 28:
            if not s:
                print('Part 1:', r[3])
            if r[3] in s:
                print('Part 2:', m)
                break
            else:
                s.add(r[3])
                m = r[3]
        runner(r, *code)
        r[ip] += 1

def main1():
    data = [
        #ip 2
        "seti 123 0 3",
        "bani 3 456 3",
        "eqri 3 72 3",
        "addr 3 2 2",
        "seti 0 0 2",
        "seti 0 6 3",
        "bori 3 65536 4",
        "seti 2176960 8 3",
        "bani 4 255 1",
        "addr 3 1 3",
        "bani 3 16777215 3",
        "muli 3 65899 3",
        "bani 3 16777215 3",
        "gtir 256 4 1",
        "addr 1 2 2",
        "addi 2 1 2",
        "seti 27 7 2",
        "seti 0 9 1",
        "addi 1 1 5",
        "muli 5 256 5",
        "gtrr 5 4 5",
        "addr 5 2 2",
        "addi 2 1 2",
        "seti 25 7 2",
        "addi 1 1 1",
        "seti 17 2 2",
        "setr 1 7 4",
        "seti 7 9 2",
        "eqrr 3 0 1",
        "addr 1 2 2",
        "seti 5 9 2",
    ]
    data = [parse(line) for line in data]
    program(0, 2, data)

def main2():
    """ Reverse engineered code of the program from main1()
        (non-essential parts are excluded)
    """
    s = set()
    m = None
    r3 = 0
    r0 = 0
    while True:
        r4 = r3 | 65536 # pow(2, 16)
        r3 = 2176960
        while True:
            r3 = (((r3 + (r4 & 0xff)) & 0xffffff) * 65899) & 0xffffff
            if 256 > r4:
                break
            r4 = r4 // 256
        if not s:
            print('Part 1:', r3)
        if r3 in s:
            print('Part 2:', m)
            break
        else:
            s.add(r3)
            m = r3
        #if r3 == r0:
        #    break

if __name__ == '__main__':
    #main1()
    main2()
