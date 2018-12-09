
class Node:
    def __init__(self, val):
        self.left = None
        self.right = None
        self.val = val

    @classmethod
    def insert_between(cls, val, left_node, right_node):
        node = Node(val)
        node.set_right(right_node)
        node.set_left(left_node)
        return node

    @classmethod
    def insert_after(cls, val, left_node):
        right_node = left_node.right
        node = Node(val)
        node.set_left(left_node)
        node.set_right(right_node)
        return node

    @classmethod
    def insert_before(cls, val, right_node):
        left_node = right_node.left
        node = Node(val)
        node.set_right(right_node)
        node.set_left(left_node)
        return node

    def set_right(self, node):
        self.right = node
        node.left = self

    def set_left(self, node):
        self.left = node
        node.right = self

    def remove(self):
        left_node = self.left
        right_node = self.right
        left_node.set_right(right_node)

class NodeRightIterator:
    def __init__(self, node):
        self.node = node

    def __iter__(self):
        return self

    def __next__(self):
        if not self.node:
            raise StopIteration
        node = self.node
        self.node = self.node.right
        return node

class NodeLeftIterator:
    def __init__(self, node):
        self.node = node

    def __iter__(self):
        return self

    def __next__(self):
        if not self.node:
            raise StopIteration
        node = self.node
        self.node = self.node.left
        return node

class Solver:
    def __init__(self, nplayers):
        self.current = None
        self.scores = [0 for i in range(0, nplayers)]
        self.nplayers = nplayers
        self.root = None

    def init_node(self, val):
        node = Node(val)
        node.set_right(node)
        self.current = node
        self.root = node

    def add_score(self, tick, val):
        player = tick % self.nplayers
        self.scores[player] += val

    def tick_23(self, val):
        self.add_score(val, val)
        it = NodeLeftIterator(self.current)
        next(it)
        for i in range(0, 7):
            node = next(it)
        node.remove()
        self.add_score(val, node.val)
        self.current = node.right

    def tick_normal(self, val):
        it = NodeRightIterator(self.current)
        next(it)
        left_node = next(it)
        self.current = Node.insert_after(val, left_node)

    def tick(self, val):
        if val == 0:
            self.init_node(val)
        elif val % 23 == 0:
            self.tick_23(val)
        else:
            self.tick_normal(val)

    def print(self):
        it = NodeRightIterator(self.root)
        node = next(it)
        print(node.val, end=' ')
        while True:
            node = next(it)
            if node == self.root:
                break
            print(node.val, end=' ')
        print()

    def process(self, nturns):
        for i in range(0, nturns):
            self.tick(i)
            #self.print()

    def highscore(self):
        return max(self.scores)

    @classmethod
    def play(cls, nplayers, nturns):
        solver = cls(nplayers)
        solver.process(nturns)
        return solver.highscore()

def test1():
    assert Solver.play(9, 25) == 32
    assert Solver.play(10, 1618) == 8317
    assert Solver.play(30, 5807) == 37305

def main():
    print('Part 1:', Solver.play(418, 70769))
    print('Part 2:', Solver.play(418, 7076900))

if __name__ == '__main__':
    test1()
    main()
