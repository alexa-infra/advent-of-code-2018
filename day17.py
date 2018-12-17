import sys
import re

parse_re = re.compile(
    r'(?P<a>[xy])=(?P<av>\d+), (?P<b>[xy])=(?P<bv1>\d+)\.\.(?P<bv2>\d+)')

def parse(text):
    m = parse_re.match(text)
    d = m.groupdict()
    av = int(d['av'])
    bv1 = int(d['bv1'])
    bv2 = int(d['bv2'])
    if d['a'] == 'x':
        return av, (bv1, bv2)
    if d['a'] == 'y':
        return (bv1, bv2), av
    return None

is_block = lambda tile: tile == '#'
is_water = lambda tile: tile == '~'
is_free = lambda tile: tile == '.'
is_stream = lambda tile: tile == '|'

class Drop:
    def __init__(self, coord, direction):
        x, y = coord
        self.x = x
        self.y = y
        self.direction = direction
        self.block = False
        self.parent = None
        self.left = None

    @property
    def coord(self):
        return self.x, self.y

    def ref(self, parent, left):
        self.parent = parent
        self.left = left

def init_map(coords):
    mmap = dict()
    for x, y in coords:
        if isinstance(x, tuple):
            x1, x2 = x
            for xi in range(x1, x2 + 1):
                mmap[(xi, y)] = '#'
        elif isinstance(y, tuple):
            y1, y2 = y
            for yi in range(y1, y2 + 1):
                mmap[(x, yi)] = '#'
    dots = set(mmap.keys())
    xs = [x for x, y in dots]
    ys = [y for x, y in dots]
    xmin, xmax = min(xs) - 2, max(xs) + 2
    ymin, ymax = min(ys), max(ys)
    limits = (xmin, xmax, ymin, ymax)
    return mmap, limits

class State:

    def __init__(self, coords):
        mmap, limits = init_map(coords)
        self.map = mmap
        self.limits = limits
        vail = (500, limits[2])
        self.drops = [Drop(vail, 'D')]
        self.map[vail] = '|'

    def print(self, out=sys.stdout):
        xmin, xmax, ymin, ymax = self.limits
        for y in range(ymin-1, ymax+2):
            for x in range(xmin, xmax+1):
                dot = (x, y)
                ch = self.map.get(dot, '.')
                print(ch, end='', file=out)
            print(file=out)
        print(file=out)

    def map_limits(self, x, y):
        xmin, xmax, ymin, ymax = self.limits
        if x < xmin or x > xmax:
            return False
        if y < ymin or y > ymax:
            return False
        return True

    def tick(self):
        drop = self.drops.pop()
        self.move(drop)

    def play(self):
        i = 0
        while self.drops:
            #self.print()
            self.tick()
            i += 1
        #self.print()

    def map_at(self, x, y):
        if not self.map_limits(x, y):
            return None
        return self.map.get((x, y), '.')

    def set_map_at(self, x, y, tile):
        if not self.map_limits(x, y):
            return
        self.map[(x, y)] = tile

    def move(self, drop):
        if drop.direction == 'D':
            self.move_down(drop)
        elif drop.direction == 'L':
            self.move_left(drop)
        elif drop.direction == 'R':
            self.move_right(drop)

    def move_down(self, drop):
        x, y = drop.coord
        tile = self.map_at(x, y + 1)
        while tile is not None:
            if is_block(tile) or is_water(tile):
                drop_left = Drop((x, y), 'L')
                drop_right = Drop((x, y), 'R')
                drop_right.ref(drop, drop_left)
                self.drops.append(drop_right)
                self.drops.append(drop_left)
                break
            if is_free(tile):
                y += 1
                self.set_map_at(x, y, '|')
                drop.y = y
                tile = self.map_at(x, y + 1)
            if is_stream(tile):
                break

    def move_left(self, drop):
        x, y = drop.coord
        if is_water(self.map_at(x, y)):
            return
        tile = self.map_at(x - 1, y)
        while tile is not None:
            if is_block(tile):
                drop.block = True
                break
            if is_free(tile) or is_stream(tile):
                x -= 1
                self.set_map_at(x, y, '|')
                drop.x = x
                tile_bottom = self.map_at(x, y + 1)
                if tile_bottom is None:
                    break
                elif is_block(tile_bottom) or is_water(tile_bottom):
                    pass
                elif is_free(tile_bottom):
                    new_drop = Drop((x, y), 'D')
                    self.drops.append(new_drop)
                    break
                elif is_stream(tile_bottom):
                    break
                tile = self.map_at(x - 1, y)

    def move_right(self, drop):
        x, y = drop.coord
        if is_water(self.map_at(x, y)):
            return
        tile = self.map_at(x + 1, y)
        while tile is not None:
            if is_block(tile):
                drop.block = True
                if drop.left.block:
                    x1 = drop.left.x
                    x2 = drop.x
                    for i in range(x1, x2 + 1):
                        self.set_map_at(i, y, '~')
                    x, y = drop.parent.coord
                    new_drop = Drop((x, y - 1), 'D')
                    self.drops.append(new_drop)
                    self.set_map_at(x, y - 1, '|')
                break
            if is_free(tile) or is_stream(tile):
                x += 1
                self.set_map_at(x, y, '|')
                drop.x = x
                tile_bottom = self.map_at(x, y + 1)
                if tile_bottom is None:
                    break
                elif is_block(tile_bottom) or is_water(tile_bottom):
                    pass
                elif is_free(tile_bottom):
                    new_drop = Drop((x, y), 'D')
                    self.drops.append(new_drop)
                    break
                elif is_stream(tile_bottom):
                    break
                tile = self.map_at(x + 1, y)

    def count_water(self):
        cc, ww = 0, 0
        for ch in self.map.values():
            if is_water(ch) or is_stream(ch):
                cc += 1
            if is_water(ch):
                ww += 1
        #print(cc, ww)
        return cc, ww

    @classmethod
    def solve(cls, data):
        s = cls(data)
        s.play()
        return s.count_water()

def test1():
    text = [
        "x=495, y=2..7",
        "y=7, x=495..501",
        "x=501, y=3..7",
        "x=498, y=2..4",
        "x=506, y=1..2",
        "x=498, y=10..13",
        "x=504, y=10..13",
        "y=13, x=498..504"
    ]
    data = [parse(line) for line in text]
    assert State.solve(data) == (57, 29)

def test2():
    text = [
        "y=10, x=490..510",
        "x=490, y=5..10",
        "x=510, y=5..10",
        "y=8, x=495..505",
        "x=495, y=6..8",
        "x=505, y=6..8",
        "x=480, y=5..10",
        "x=520, y=3..10",
    ]
    data = [parse(line) for line in text]
    assert State.solve(data) == (116, 80)

def main():
    with open('day17.txt', 'r') as f:
        text = f.readlines()
    data = [parse(line) for line in text]
    cc, ww = State.solve(data)
    print('Part 1:', cc)
    print('Part 2:', ww)

if __name__ == '__main__':
    test1()
    test2()
    main()
