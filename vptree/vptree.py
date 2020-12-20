from typing import Optional, Callable, Any, List

from vptree.node import VPTreeNode


class VPTree:
    capacity: int
    distance_fn: Callable[[Any, Any], float]
    root: Optional[VPTreeNode]

    def __init__(self, distance_fn: Callable[[Any, Any], float], capacity: int = 32):
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

    def add(self, point: Any):
        self.add_list([point])

    def remove(self, point: Any):
        if self.root is None:
            return False
        removed = self.root.remove(point)
        if removed:
            self.root.anneal()
        return removed

    def contains(self, point: Any):
        if self.root is None:
            return False
        return self.root.contains(point)

    def get_within_distance(self, query: Any, max_distance: float):
        if self.root is None:
            return []
        return self.root.get_within_distance(query, max_distance)

    def get_nearest_neighbours(self, query: Any, num_neighbours: int, max_results: int = 16):
        if self.root is None:
            return []
        return self.root.get_nearest_neighbours(query, num_neighbours, max_results)
