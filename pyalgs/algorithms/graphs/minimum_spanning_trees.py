from abc import ABCMeta, abstractmethod

from pyalgs.algorithms.commons.union_find import UnionFind
from pyalgs.algorithms.commons.util import less
from pyalgs.data_structures.commons.bag import Bag
from pyalgs.data_structures.commons.priority_queue import MinPQ, IndexMinPQ
from pyalgs.data_structures.graphs.graph import EdgeWeightedGraph


class MST(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def spanning_tree(self):
        pass


class KruskalMST(MST):
    tree = None

    def __init__(self, G):
        if not isinstance(G, EdgeWeightedGraph):
            raise ValueError('Graph must be edge weighted and undirected to run MST')
        minpq = MinPQ.create()
        self.tree = Bag()
        for e in G.edges():
            minpq.enqueue(e)

        uf = UnionFind.create(G.vertex_count())

        while not minpq.is_empty() and self.tree.size() < G.vertex_count() - 1:
            e = minpq.del_min()
            v = e.either()
            w = e.other(v)
            if not uf.connected(v, w):
                uf.union(v, w)
                self.tree.add(e)

    def spanning_tree(self):
        return self.tree.iterate()


class LazyPrimMST(MST):
    tree = None
    marked = None
    minpq = None

    def __init__(self, G):
        if not isinstance(G, EdgeWeightedGraph):
            raise ValueError('Graph must be edge weighted and undirected to run MST')
        self.minpq = MinPQ.create()
        self.tree = Bag()
        vertex_count = G.vertex_count()
        self.marked = [False] * vertex_count
        self.visit(G, 0)

        while not self.minpq.is_empty() and self.tree.size() < vertex_count - 1:
            edge = self.minpq.del_min()
            v = edge.either()
            w = edge.other(v)
            if self.marked[v] and self.marked[w]:
                continue
            self.tree.add(edge)
            if not self.marked[v]:
                self.visit(G, v)
            if not self.marked[w]:
                self.visit(G, w)

    def visit(self, G, v):
        self.marked[v] = True
        for e in G.adj(v):
            w = e.other(v)
            if not self.marked[w]:
                self.minpq.enqueue(e)

    def spanning_tree(self):
        return self.tree.iterate()


class EagerPrimMST(MST):
    path = None
    pq = None
    marked = None

    def __init__(self, G):
        if not isinstance(G, EdgeWeightedGraph):
            raise ValueError('Graph must be edge weighted and undirected to run MST')
        vertex_count = G.vertex_count()
        self.pq = IndexMinPQ(vertex_count)
        self.path = Bag()
        self.marked = [False] * vertex_count

        self.visit(G, 0)

        while not self.pq.is_empty() and self.path.size() < vertex_count - 1:
            e = self.pq.min_key()
            w = self.pq.del_min()
            self.path.add(e)
            if not self.marked[w]:
                self.visit(G, w)

    def visit(self, G, v):
        self.marked[v] = True
        for e in G.adj(v):
            w = e.other(v)
            if not self.marked[w]:
                if self.pq.contains_index(w):
                    old_e = self.pq.get(w)
                    if less(e, old_e):
                        self.pq.decrease_key(w, e)
                else:
                    self.pq.insert(w, e)

    def spanning_tree(self):
        return self.path.iterate()
