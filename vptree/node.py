import copy
import random
from typing import Optional, Any, List, Callable

from vptree.priority_queue import PriorityQueue


class VPTreeNode:
    capacity: int
    distance_fn: Callable[[Any, Any], float]
    vantage_point: Any
    threshold: float
    closer: Optional['VPTreeNode']
    farther: Optional['VPTreeNode']
    points: Optional[List[Any]]

    def __init__(self, points: List[Any], distance_fn: Callable[[Any, Any], float], capacity: int = 32):
        self.capacity = capacity
        self.distance_fn = distance_fn
        self.points = copy.deepcopy(points)
        self.vantage_point = random.choice(self.points)
        self.closer = None
        self.farther = None
        self.threshold = 0.0
        self.partition()

    def partition(self):
        if self.points is None:
            if self.closer.size() == 0 or self.farther.size() == 0:
                self.points = copy.deepcopy(self.closer.points)
                self.points += self.farther.points

                self.closer = None
                self.farther = None

                self.partition()
            else:
                self.closer.partition()
                self.farther.partition()
        elif len(self.points) > self.capacity:
            self._partition_points()

    def size(self) -> int:
        if self.points is None:
            return self.closer.size() + self.farther.size()
        return len(self.points)

    def _partition_points(self):
        self.threshold = self._select_threshold()

        partition_idx = self._get_partition_idx()
        if partition_idx is None:
            self.closer = None
            self.farther = None
        else:
            self.closer = VPTreeNode(self.points[:partition_idx], self.distance_fn, self.capacity)
            self.farther = VPTreeNode(self.points[partition_idx:], self.distance_fn, self.capacity)
            self.points = None

    def add(self, point: Any):
        if self.points is None:
            self._get_child_for_point(point).add(point)
        else:
            self.points.append(point)

    def remove(self, point: Any):
        if self.points is None:
            return self._get_child_for_point(point).remove(point)
        else:
            try:
                self.points.remove(point)
                return True
            except ValueError:
                return False

    def _get_child_for_point(self, point: Any) -> 'VPTreeNode':
        if self.distance_fn(self.vantage_point, point) > self.threshold:
            return self.farther
        return self.closer

    def contains(self, point: Any):
        if self.points is None:
            return self._get_child_for_point(point).contains(point)
        return point in self.points

    def _select_threshold(self):
        if len(self.points) > 32:
            sampled_points = random.sample(self.points, 32)
        else:
            sampled_points = copy.deepcopy(self.points)
        left = 0
        right = len(sampled_points) - 1
        median_idx = len(sampled_points) // 2
        while left != right:
            pivot_idx = left + random.randint(0, right - left)
            pivot_distance = self.distance_fn(self.vantage_point, sampled_points[pivot_idx])

            sampled_points[pivot_idx], sampled_points[right] = sampled_points[right], sampled_points[pivot_idx]

            store_idx = left

            for i in range(left, right):
                if self.distance_fn(self.vantage_point, sampled_points[i]) < pivot_distance:
                    sampled_points[store_idx], sampled_points[i] = sampled_points[i], sampled_points[store_idx]
                    store_idx += 1

            sampled_points[pivot_idx], sampled_points[right] = sampled_points[right], sampled_points[pivot_idx]

            if store_idx == median_idx:
                break
            elif store_idx < median_idx:
                left = store_idx + 1
            else:
                right = store_idx - 1

        return self.distance_fn(self.vantage_point, sampled_points[median_idx])

    def _get_partition_idx(self) -> Optional[int]:
        left = 0
        right = len(self.points) - 1
        while left <= right:
            if self.distance_fn(self.vantage_point, self.points[left]) > self.threshold:
                while right >= left:
                    if self.distance_fn(self.vantage_point, self.points[right]) <= self.threshold:
                        self.points[left], self.points[right] = self.points[right], self.points[left]
                        right -= 1
                        break
                    right -= 1
            left += 1

        if self.distance_fn(self.vantage_point, self.points[left - 1]) > self.threshold:
            first_index_past_threshold = left - 1
        else:
            first_index_past_threshold = left

        if self.distance_fn(self.vantage_point, self.points[0]) <= self.threshold < self.distance_fn(
                self.vantage_point, self.points[-1]):
            return first_index_past_threshold

        return None

    def get_nearest_neighbours(self, point: Any, num_neighbours: int, max_results: int) -> List[Any]:
        heap = PriorityQueue(point, self.distance_fn, max_results)
        self._get_nearest_neighbours(heap, point, num_neighbours, max_results)

        return heap.list()

    def _get_nearest_neighbours(self, heap: PriorityQueue, point: Any, num_neighbours: int, max_results: int):
        if self.points is None:
            first_node = self._get_child_for_point(point)
            first_node._get_nearest_neighbours(heap, point, num_neighbours, max_results)

            distance_from_vantage_point_to_query_point = self.distance_fn(self.vantage_point, point)
            distance_from_query_point_to_farthest_point = self.distance_fn(point, heap.peek())
            if first_node is self.closer:
                distance_from_query_point_to_threshold = self.threshold - distance_from_vantage_point_to_query_point
                if distance_from_query_point_to_farthest_point > distance_from_query_point_to_threshold:
                    self.farther._get_nearest_neighbours(heap, point, num_neighbours, max_results)
            else:
                distance_from_query_point_to_threshold = distance_from_vantage_point_to_query_point - self.threshold
                if distance_from_query_point_to_threshold <= distance_from_query_point_to_farthest_point:
                    self.closer._get_nearest_neighbours(heap, point, num_neighbours, max_results)
        else:
            for p in self.points:
                heap.push(p)

    def get_within_distance(self, point: Any, max_distance: float) -> List[Any]:
        result = []
        self._get_within_distance(result, point, max_distance)
        return result

    def _get_within_distance(self, result: List[Any], point: Any, max_distance: float):
        if self.points is None:
            distance_from_vantage_point_to_query_point = self.distance_fn(self.vantage_point, point)

            if distance_from_vantage_point_to_query_point <= self.threshold + max_distance:
                self.closer._get_within_distance(result, point, max_distance)

            if distance_from_vantage_point_to_query_point + max_distance > self.threshold:
                self.farther._get_within_distance(result, point, max_distance)
        else:
            for p in self.points:
                if self.distance_fn(point, p) <= max_distance:
                    result.append(p)
