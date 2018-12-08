
class Node:
    def __init__(self, parent):
        self.parent = parent
        self.num_children = None
        self.num_meta = None
        self.children = []
        self.meta = []

    @classmethod
    def read(cls, it, parent=None):
        node = cls(parent)
        node.num_children = next(it)
        node.num_meta = next(it)
        #print('{} {}'.format(node.num_children, node.num_meta))
        return node

    def read_meta(self, it):
        for i in range(0, self.num_meta):
            self.meta.append(next(it))

    @property
    def children_complete(self):
        return self.num_children == len(self.children)

    @property
    def meta_complete(self):
        return self.num_meta == len(self.meta)

    @property
    def complete(self):
        return self.children_complete and self.meta_complete

    @property
    def has_parent(self):
        return self.parent is not None

    def checksum(self):
        cs = sum(self.meta)
        for child in self.children:
            cs += child.checksum()
        return cs

    def checksum2(self):
        if not self.children:
            return sum(self.meta)
        cs = 0
        for meta in self.meta:
            if meta == 0 or meta > self.num_children:
                continue
            child = self.children[meta-1]
            cs += child.checksum2()
        return cs

def buildTree(text):
    data = text.split(' ')
    idata = list(map(int, data))
    it = iter(idata)
    node = root = Node.read(it)
    while not node.complete or node.has_parent:
        if not node.children_complete:
            child = Node.read(it, node)
            node.children.append(child)
            node = child
        elif not node.meta_complete:
            node.read_meta(it)
        elif node.has_parent:
            node = node.parent
    return root

def test1():
    text = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
    node = buildTree(text)
    assert node.checksum() == 138

def test2():
    text = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
    node = buildTree(text)
    assert node.checksum2() == 66

def main():
    with open('day8.txt', 'r') as f:
        text = f.read()
    node = buildTree(text)
    print('Part 1:', node.checksum())
    print('Part 2:', node.checksum2())

if __name__ == '__main__':
    test1()
    test2()
    main()
