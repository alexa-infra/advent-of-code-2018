import re
from copy import deepcopy

parse_re = re.compile(
    r'(?P<units>\d+) units each with (?P<hp>\d+) hit points'
    r' (?P<prop>[a-z ,;\(\)]+)?'
    r' ?with an attack that does (?P<dmg>\d+) (?P<dmgtype>\w+) damage'
    r' at initiative (?P<initiative>\d+)'
)

parse_weak_re = re.compile(r'weak to ([a-z ,]+)')
parse_immune_re = re.compile(r'immune to ([a-z ,]+)')

def make_group(text):
    d = parse_re.match(text)
    if not d:
        print(text)
        assert False
    d = d.groupdict()
    if 'prop' in d and d['prop'] is not None:
        prop = d['prop']
        d1 = parse_weak_re.search(prop)
        d2 = parse_immune_re.search(prop)
        d['weak'] = d1.group(1) if d1 else ''
        d['immune'] = d2.group(1) if d2 else ''
    else:
        d['weak'] = ''
        d['immune'] = ''
    return Group(d)

def parse(lines):
    immune_system, infection = False, False
    immuneGroups = []
    infectionGroups = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        elif line.startswith('Immune System'):
            immune_system, infection = True, False
        elif line.startswith('Infection'):
            immune_system, infection = False, True
        else:
            gr = make_group(line)
            if immune_system:
                gr.type = 1
                gr.name = len(immuneGroups) + 1
                immuneGroups.append(gr)
            elif infection:
                gr.type = 2
                gr.name = len(infectionGroups) + 1
                infectionGroups.append(gr)
    return immuneGroups, infectionGroups

class Group:
    def __init__(self, data):
        self.__dict__.update(data)
        self.units = int(self.units)
        self.hp = int(self.hp)
        self.weak = [x.strip() for x in self.weak.split(',')]
        self.immune = [x.strip() for x in self.immune.split(',')]
        self.dmg = int(self.dmg)
        self.initiative = int(self.initiative)
        self.type = None
        self.attacking = None
        self.defending = None
        self.name = None

    def __repr__(self):
        return 'type {} name {}'.format(self.type, self.name)

    @property
    def atk(self):
        return self.dmg * self.units

    @property
    def totalHP(self):
        return self.units * self.hp

    @property
    def isAlive(self):
        return self.units > 0

def estimateDmg(attacker, defender):
    if attacker.dmgtype in defender.immune:
        return 0 # zero dmg
    elif attacker.dmgtype in defender.weak:
        return attacker.atk * 2 # double dmg
    else:
        return attacker.atk # normal dmg

def doDamage(attacker, defender):
    dmg = estimateDmg(attacker, defender)
    unitsKilled = min(defender.units, dmg // defender.hp)
    defender.units -= unitsKilled
    return unitsKilled
    #print(attacker, 'attacks', defender, 'kills', unitsKilled)

class State:
    def __init__(self, data1, data2):
        self.groups = deepcopy(data1) + deepcopy(data2)

    @property
    def aliveArmy(self):
        func = lambda gr: gr.isAlive
        return filter(func, self.groups)

    @property
    def groupsByAtk(self):
        func = lambda gr: (gr.atk, gr.initiative)
        return sorted(self.aliveArmy, key=func, reverse=True)

    @property
    def groupsByInitiative(self):
        func = lambda gr: gr.initiative
        return sorted(self.aliveArmy, key=func, reverse=True)

    def armyByType(self, type):
        func = lambda gr: gr.type == type
        return filter(func, self.aliveArmy)

    def defendingGroups(self, attacker):
        deftype = 1 if attacker.type == 2 else 2
        defenders = filter(lambda gr: gr.defending is None,
                           self.armyByType(deftype))
        defenders = filter(lambda gr: estimateDmg(attacker, gr) > 0, defenders)
        func = lambda gr: (estimateDmg(attacker, gr), gr.atk, gr.initiative)
        return sorted(defenders, key=func, reverse=True)

    @property
    def warOver(self):
        army1 = list(self.armyByType(1))
        army2 = list(self.armyByType(2))
        return not army1 or not army2

    @property
    def getNumAlive(self):
        army = list(self.aliveArmy)
        return sum(gr.units for gr in army)

    def tick(self):
        groups = list(self.groupsByAtk)
        for gr in groups:
            defenders = self.defendingGroups(gr)
            if defenders:
                defender = defenders[0]
                defender.defending = gr
                gr.attacking = defender
        unitsKilled = 0
        for gr in self.groupsByInitiative:
            if not gr.isAlive:
                continue
            if not gr.attacking:
                continue
            defender = gr.attacking
            if not defender.isAlive:
                continue
            unitsKilled += doDamage(gr, defender)
        for gr in groups:
            gr.defending = None
            gr.attacking = None
        return unitsKilled > 0

    def battle(self):
        while not self.warOver:
            hasDmg = self.tick()
            if not hasDmg:
                break
        army1 = list(self.armyByType(1))
        army2 = list(self.armyByType(2))
        return sum(gr.units for gr in army1), sum(gr.units for gr in army2)

    @classmethod
    def findBoost(cls, data1, data2):
        state = cls(data1, data2)
        data = deepcopy(state.groups)
        boost = 0
        while True:
            groups = deepcopy(data)
            for gr in groups:
                if gr.type == 1:
                    gr.dmg += boost
            state.groups = groups
            left, right = state.battle()
            #print(boost, left, right)
            if left > 0 and right == 0:
                return left
            boost += 1

    @classmethod
    def play(cls, data1, data2):
        state = cls(data1, data2)
        #print([gr.units for gr in state.groups])
        left, right = state.battle()
        #print([gr.units for gr in state.groups])
        return (left, right)

def test1():
    with open('day24-1.txt', 'r') as f:
        lines = f.readlines()
    data1, data2 = parse(lines)
    assert State.play(data1, data2) == (0, 5216)
    assert State.findBoost(data1, data2) == 51

def main():
    with open('day24.txt', 'r') as f:
        lines = f.readlines()
    data1, data2 = parse(lines)
    print('Part 1:', max(State.play(data1, data2)))
    print('Part 2:', State.findBoost(data1, data2))

if __name__ == '__main__':
    test1()
    main()
