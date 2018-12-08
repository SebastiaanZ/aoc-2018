class Node:
    def __init__(self, n_children, n_metadata, parent):
        self.n_children = n_children
        self.parent = parent
        self.n_metadata = n_metadata
        self.children = list()
        self.metadata: list

    @property
    def unprocessed_children(self):
        return bool(self.n_children - len(self.children))

    def __len__(self):
        return len(self.children)

    def __lt__(self, other):
        return len(self) < len(other)

    @property
    def value(self):
        if self.children:
            return sum(self.children[i-1].value for i in self.metadata
                       if (i-1) < self.n_children)
        else:
            return sum(self.metadata)
