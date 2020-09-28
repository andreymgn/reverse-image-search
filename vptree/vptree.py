import pickle
from typing import Optional, Callable, Any, List

from vptree.node import VPTreeNode


class VPTree:
    root: Optional[VPTreeNode]

    def __init__(self, distance_fn: Callable[[Any, Any], float], capacity=32):
        self.root = None
        self.distance_fn = distance_fn
        self.capacity = capacity

    def add_list(self, points: List[Any]):
        if self.root is None:
            self.root = VPTreeNode(points, self.distance_fn, self.capacity)
            return
        for point in points:
            self.root.add(point)
        self.root.anneal()

    def add(self, point):
        self.add_list([point])

    def remove(self, point):
        if self.root is None:
            return False
        removed = self.root.remove(point)
        if removed:
            self.root.anneal()
        return removed

    def contains(self, point):
        if self.root is None:
            return False
        return self.root.contains(point)

    def get_within_distance(self, query, max_distance):
        if self.root is None:
            return []
        return self.root.get_within_distance(query, max_distance)

    def get_nearest_neighbours(self, query, num_neighbours, max_results=16):
        if self.root is None:
            return []
        return self.root.get_nearest_neighbours(query, num_neighbours, max_results)


def encode(tree: VPTree, path):
    with open(path, 'wb') as f:
        pickle.dump(tree, f)


def decode(path) -> VPTree:
    with open(path, 'rb') as f:
        return pickle.load(f)
