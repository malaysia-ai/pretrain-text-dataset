class UnionFind:
    """
    A data structure for maintaining disjoint sets. This helps build connected components for given duplicate pairs.

    Examples
    --------
    >>> uf = UnionFind()
    >>> uf.union(1, 2)
    >>> uf.union(2, 3)
    >>> uf.union(4, 5)
    >>> uf.find(1)
    1
    >>> uf.find(2)
    1
    >>> uf.find(3)
    1
    >>> uf.find(4)
    4
    >>> uf.find(5)
    4
    """

    def __init__(self):
        self.parent = {}

    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x
            return x

        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])

        return self.parent[x]

    def union(self, x, y):
        px = self.find(x)
        py = self.find(y)
        self.parent[px] = self.parent[py] = min(px, py)