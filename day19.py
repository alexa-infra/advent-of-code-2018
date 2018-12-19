from day16 import opcodes

def runner(r, name, a, b, c):
    #print(r, end=' ')
    #print(name, a, b, c, end=' ')
    opcode = opcodes[name]
    opcode(r, None, a, b, c)
    #print(r,)

def program(r0, ip, codes):
    r = [r0, 0, 0, 0, 0, 0]
    while r[ip] >= 0 and r[ip] < len(codes):
        code = codes[r[ip]]
        runner(r, *code)
        r[ip] += 1
    return r[0]

def parse(line):
    arr = line.split(' ')
    return arr[0], int(arr[1]), int(arr[2]), int(arr[3])

def test1():
    data = [
        #ip 0
        "seti 5 0 1",
        "seti 6 0 2",
        "addi 0 1 0",
        "addr 1 2 3",
        "setr 1 0 0",
        "seti 8 0 4",
        "seti 9 0 5",
    ]
    data = [parse(line) for line in data]
    assert program(0, 0, data) == 7

def main1():
    """ Straight run of the program, its very slow, part 2 takes too much time
    """
    data = [
        #ip 3
        "addi 3 16 3",
        "seti 1 8 4",
        "seti 1 4 5",
        "mulr 4 5 1",
        "eqrr 1 2 1",
        "addr 1 3 3",
        "addi 3 1 3",
        "addr 4 0 0",
        "addi 5 1 5",
        "gtrr 5 2 1",
        "addr 3 1 3",
        "seti 2 1 3",
        "addi 4 1 4",
        "gtrr 4 2 1",
        "addr 1 3 3",
        "seti 1 3 3",
        "mulr 3 3 3",
        "addi 2 2 2",
        "mulr 2 2 2",
        "mulr 3 2 2",
        "muli 2 11 2",
        "addi 1 3 1",
        "mulr 1 3 1",
        "addi 1 17 1",
        "addr 2 1 2",
        "addr 3 0 3",
        "seti 0 3 3",
        "setr 3 0 1",
        "mulr 1 3 1",
        "addr 3 1 1",
        "mulr 3 1 1",
        "muli 1 14 1",
        "mulr 1 3 1",
        "addr 2 1 2",
        "seti 0 8 0",
        "seti 0 9 3",
    ]
    data = [parse(line) for line in data]
    print('Part 1:', program(0, 3, data))
    #print('Part 2:', program(1, 3, data))

def main2():
    """ Reverse-engineered code of the program from main1() """
    def getSumDiv(n):
        s = 0
        for i in range(1, n // 2):
            if n % i == 0:
                s += i
        s += n
        return s
    r2 = 2 * 2 * 19 * 11
    r2 += 3 * 22 + 17
    print('Part 1:', getSumDiv(r2))
    r2 += (27 * 28 + 29) * 30 * 14 * 32
    print('Part 2:', getSumDiv(r2))

if __name__ == '__main__':
    test1()
    main1()
    main2()
