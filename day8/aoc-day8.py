from collections import deque
from tree import Node


with open("day8-input.txt") as f:
    data = deque(int(x) for x in f.read().strip().split())


tree = list()
header = True
parent = None
checksum = 0

while data:
    if header:
        n_children = data.popleft()
        n_metadata = data.popleft()
        node = Node(n_children, n_metadata, parent)
        tree.append(node)
        if parent is not None:
            parent.children.append(node)

    if node.unprocessed_children:
        parent = node
        header = True
    else:
        node.metadata = [data.popleft() for i in range(node.n_metadata)]
        checksum += sum(node.metadata)
        if parent is None:
            header = True
            continue
        node = parent
        parent = node.parent
        header = False


print(checksum)
print(tree[0].value)








