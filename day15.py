
ELF, GOBLIN, WALL, EMPTY = tuple(range(4))

def iterCell(coord):
    x, y = coord
    yield x, y - 1
    yield x - 1, y
    yield x + 1, y
    yield x, y + 1

def initMap(data, atk_e=3, atk_g=3):
    mapp = dict()
    units = list()
    for y, line in enumerate(data):
        for x, ch in enumerate(line):
            coord = (x, y)
            if ch == '#':
                mapp[coord] = WALL
            elif ch == 'G':
                unit = Unit(GOBLIN, x, y, atk_g)
                units.append(unit)
                mapp[coord] = unit
            elif ch == 'E':
                unit = Unit(ELF, x, y, atk_e)
                units.append(unit)
                mapp[coord] = unit
            elif ch == '.':
                mapp[coord] = EMPTY
    return mapp, units

def iterNeighbors(mapp, cell, friend, enemy):
    for coord in iterCell(cell):
        neighbor = mapp.get(coord)
        if not neighbor:
            continue
        if isinstance(neighbor, Unit):
            if neighbor.type == friend:
                continue
            elif neighbor.type == enemy:
                yield coord
        elif neighbor is WALL:
            continue
        elif neighbor is EMPTY:
            yield coord

def recostructPath(cameFrom, current):
    total_path = [current]
    while current in cameFrom:
        current = cameFrom[current]
        total_path.append(current)
    return total_path[:-1]

class State:
    def __init__(self, data, atk_e=3, atk_g=3):
        mapp, units = initMap(data, atk_e, atk_g)
        self.map = mapp
        self.units = units
        self.ymax = len(data)
        self.xmax = len(data[0])

    @property
    def aliveUnitsQ(self):
        return filter(lambda u: not u.dead, self.units)

    @property
    def anyDeadElf(self):
        elves = filter(lambda u: u.type == ELF, self.units)
        return any(filter(lambda u: u.dead, elves))

    @property
    def allElvesDead(self):
        elves = filter(lambda u: u.type == ELF, self.units)
        return all(map(lambda u: u.dead, elves))

    @property
    def allGoblinsDead(self):
        goblins = filter(lambda u: u.type == GOBLIN, self.units)
        return all(map(lambda u: u.dead, goblins))

    def findEnemy(self, unit):
        """ Dijkstra-like algorithm """
        friend = unit.type
        enemy = GOBLIN if friend == ELF else ELF

        openSet = [unit.coord]
        closedSet = []
        cameFrom = dict()

        while openSet:
            current = openSet.pop(0)
            closedSet.append(current)
            for nextEl in iterNeighbors(self.map, current, friend, enemy):
                if nextEl in closedSet:
                    continue
                if nextEl not in openSet:
                    openSet.append(nextEl)
                    cameFrom[nextEl] = current
                m = self.map.get(nextEl)
                if isinstance(m, Unit) and m.type == enemy:
                    return recostructPath(cameFrom, nextEl)
        return None

    def closestEnemy(self, unit):
        friend = unit.type
        enemy = GOBLIN if friend == ELF else ELF

        enemies = []
        for coord in iterNeighbors(self.map, unit.coord, friend, enemy):
            neighbor = self.map.get(coord)
            if isinstance(neighbor, Unit) and neighbor.type == enemy:
                enemies.append(neighbor)
        return min(enemies, key=lambda u: (u.hp, u.coord[1], u.coord[0]))

    def move(self, unit, coord):
        oldCoord = unit.coord
        unit.coord = coord
        self.map[oldCoord] = EMPTY
        self.map[coord] = unit

    def fight(self, attacker, defender):
        defender.hp -= attacker.atk
        if defender.hp <= 0:
            self.kill(defender)

    def kill(self, unit):
        self.map[unit.coord] = EMPTY
        unit.dead = True

    def turn(self, unit):
        path = self.findEnemy(unit)
        if not path:
            return
        dist = len(path)
        if dist > 1:
            target = path[-1]
            self.move(unit, target)
        if dist <= 2:
            enemy = self.closestEnemy(unit)
            self.fight(unit, enemy)

    def hasAliveEnemies(self, unit):
        enemy = GOBLIN if unit.type == ELF else ELF
        return any(filter(lambda u: u.type == enemy, self.aliveUnitsQ))

    def tick(self):
        units = list(self.aliveUnitsQ)
        units.sort(key=lambda u: (u.coord[1], u.coord[0]))
        for unit in units:
            if unit.dead:
                continue
            if not self.hasAliveEnemies(unit):
                return False
            self.turn(unit)
        return True

    def print(self):
        for y in range(0, self.ymax+1):
            for x in range(0, self.xmax + 1):
                coord = (x, y)
                el = self.map.get(coord)
                if el is WALL:
                    print('#', end='')
                elif el is EMPTY:
                    print('.', end='')
                elif isinstance(el, Unit):
                    if el.type == GOBLIN:
                        print('G', end='')
                    elif el.type == ELF:
                        print('E', end='')
            print()
        print()

    def playUntilAnyWin(self):
        n = 0
        #self.print()
        while True:
            if self.tick():
                n += 1
            #self.print()
            if self.allGoblinsDead or self.allElvesDead:
                return n

    def playUntilElvesWin(self):
        n = 0
        while True:
            if self.tick():
                n += 1
            if self.anyDeadElf:
                return False, n
            if self.allGoblinsDead:
                return True, n

    @classmethod
    def solve1(cls, data):
        s = cls(data)
        n = s.playUntilAnyWin()
        sum_hp = sum(map(lambda u: u.hp, s.aliveUnitsQ))
        return sum_hp * n

    @classmethod
    def solve2(cls, data):
        atk_e = 4
        while True:
            s = cls(data, atk_e=atk_e)
            ret, n = s.playUntilElvesWin()
            if ret:
                break
            atk_e += 1
        sum_hp = sum(map(lambda u: u.hp, s.aliveUnitsQ))
        return sum_hp * n

class Unit:
    def __init__(self, atype, x, y, atk):
        self.type = atype
        self.hp = 200
        self.dead = False
        self.coord = (x, y)
        self.atk = atk

def test1():
    tests = {
        'day15-1.txt': 27730,
        'day15-2.txt': 36334,
        'day15-3.txt': 39514,
        'day15-4.txt': 27755,
        'day15-5.txt': 28944,
        'day15-6.txt': 18740,
    }
    for filename, value in tests.items():
        with open(filename, 'r') as f:
            data = f.readlines()
        data = [list(line.strip()) for line in data]
        assert State.solve1(data) == value, filename

def test2():
    tests = {
        'day15-1.txt': 4988,
        'day15-2.txt': 29064,
        'day15-3.txt': 31284,
        'day15-4.txt': 3478,
        'day15-5.txt': 6474,
        'day15-6.txt': 1140,
    }
    for filename, value in tests.items():
        with open(filename, 'r') as f:
            data = f.readlines()
        data = [list(line.strip()) for line in data]
        assert State.solve2(data) == value, filename

def main():
    with open('day15.txt', 'r') as f:
        data = f.readlines()
    data = [list(line.strip()) for line in data]
    print('Part 1:', State.solve1(data))
    print('Part 2:', State.solve2(data))

if __name__ == '__main__':
    test1()
    test2()
    main()
