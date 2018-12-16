import re
from collections import defaultdict

int_re = re.compile(r'-?\d+')

class OpCodes:
    @staticmethod
    def addr(r, n, a, b, c):
        r[c] = r[a] + r[b]

    @staticmethod
    def addi(r, n, a, b, c):
        r[c] = r[a] + b

    @staticmethod
    def mulr(r, n, a, b, c):
        r[c] = r[a] * r[b]

    @staticmethod
    def muli(r, n, a, b, c):
        r[c] = r[a] * b

    @staticmethod
    def banr(r, n, a, b, c):
        r[c] = r[a] & r[b]

    @staticmethod
    def bani(r, n, a, b, c):
        r[c] = r[a] & b

    @staticmethod
    def borr(r, n, a, b, c):
        r[c] = r[a] | r[b]

    @staticmethod
    def bori(r, n, a, b, c):
        r[c] = r[a] | b

    @staticmethod
    def setr(r, n, a, b, c):
        r[c] = r[a]

    @staticmethod
    def seti(r, n, a, b, c):
        r[c] = a

    @staticmethod
    def gtir(r, n, a, b, c):
        r[c] = 1 if a > r[b] else 0

    @staticmethod
    def gtri(r, n, a, b, c):
        r[c] = 1 if r[a] > b else 0

    @staticmethod
    def gtrr(r, n, a, b, c):
        r[c] = 1 if r[a] > r[b] else 0

    @staticmethod
    def eqir(r, n, a, b, c):
        r[c] = 1 if a == r[b] else 0

    @staticmethod
    def eqri(r, n, a, b, c):
        r[c] = 1 if r[a] == b else 0

    @staticmethod
    def eqrr(r, n, a, b, c):
        r[c] = 1 if r[a] == r[b] else 0

opcodes = {
    'addr': OpCodes.addr,
    'addi': OpCodes.addi,
    'mulr': OpCodes.mulr,
    'muli': OpCodes.muli,
    'banr': OpCodes.banr,
    'bani': OpCodes.bani,
    'borr': OpCodes.borr,
    'bori': OpCodes.bori,
    'setr': OpCodes.setr,
    'seti': OpCodes.seti,
    'gtri': OpCodes.gtri,
    'gtir': OpCodes.gtir,
    'gtrr': OpCodes.gtrr,
    'eqri': OpCodes.eqri,
    'eqir': OpCodes.eqir,
    'eqrr': OpCodes.eqrr,
}

def opcodeChecker(before, code, after):
    names = []
    for name, op in opcodes.items():
        r = before.copy()
        op(r, *code)
        if r == after:
            names.append(name)
    return names

def test1():
    before = [3, 2, 1, 1]
    code = [9, 2, 1, 2]
    after = [3, 2, 2, 1]
    names = opcodeChecker(before, code, after)
    assert len(names) == 3

def parseCodeTests(lines):
    tests = []
    for i in range(0, len(lines), 4):
        before_txt = lines[i]
        code_txt = lines[i+1]
        after_txt = lines[i+2]
        before = [int(x) for x in int_re.findall(before_txt)]
        code = [int(x) for x in int_re.findall(code_txt)]
        after = [int(x) for x in int_re.findall(after_txt)]
        tests.append((before, code, after))
    return tests

def main1():
    with open('day16-1.txt', 'r') as f:
        lines = f.readlines()
    tests = parseCodeTests(lines)
    m = 0
    for test in tests:
        n = len(opcodeChecker(*test))
        if n >= 3:
            m += 1
    print('Part 1:', m)

def learnOpCodes():
    with open('day16-1.txt', 'r') as f:
        lines = f.readlines()
    tests = parseCodeTests(lines)
    opcode_names = dict()
    known = dict()
    for name, op in opcodes.items():
        opcode_names[name] = defaultdict(int)
    for test in tests:
        names = opcodeChecker(*test)
        code = test[1]
        opc = code[0]
        for name in names:
            opcode_names[name][opc] += 1
    while opcode_names:
        for name, dd in opcode_names.items():
            if len(dd) == 1:
                kname = list(dd.keys())[0]
                known[kname] = name
                break
        for name, dd in opcode_names.items():
            if kname in dd:
                del dd[kname]
        opcode_names = {k: v for k, v in opcode_names.items() if v}
    assert len(opcodes) == len(known)
    return known

def main2():
    known_names = learnOpCodes()
    with open('day16-2.txt', 'r') as f:
        lines = f.readlines()
    r = [0, 0, 0, 0]
    for line in lines:
        opcode = [int(x) for x in int_re.findall(line)]
        idx = opcode[0]
        name = known_names[idx]
        op = opcodes[name]
        op(r, *opcode)
    print('Part 2:', r[0])
    print(known_names)

if __name__ == '__main__':
    test1()
    main1()
    main2()
