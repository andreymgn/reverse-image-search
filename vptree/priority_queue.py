import heapq
from functools import cmp_to_key
from typing import Any, Callable, List


class PriorityQueue:
    heap: List[Any]
    max_distance: float
    max_entries: int
    distance_fn: Callable[[Any, Any], float]
    query: Any

    def __init__(self, query: Any, distance_fn: Callable[[Any, Any], float], max_entries: int):
        self.query = query
        self.distance_fn = distance_fn
        self.max_entries = max_entries
        self.max_distance = 0.0
        self.heap = []

    def push(self, point: Any):
        added = False
        if len(self.heap) < self.max_entries:
            heapq.heappush(self.heap, (-self.distance_fn(self.query, point), point))
            added = True
        else:
            distance_to_new_point = self.distance_fn(self.query, point)
            if distance_to_new_point < self.max_distance:
                heapq.heappop(self.heap)
                heapq.heappush(self.heap, (-distance_to_new_point, point))
                added = True
        if added:
            self.max_distance = self.distance_fn(self.query, self.heap[0][1])

    def peek(self):
        return self.heap[0][1]

    def list(self):
        result = []
        for v in self.heap:
            result.append(v[1])

        return sorted(result, key=cmp_to_key(compare_dist(lambda p: self.distance_fn(self.query, p))))

    def __getitem__(self, item):
        return self.heap[item]


def compare_dist(dist_fn: Callable[[Any], float]):
    def compare(x: Any, y: Any):
        if dist_fn(x) < dist_fn(y):
            return -1
        elif dist_fn(y) < dist_fn(x):
            return 1
        else:
            return 0

    return compare
