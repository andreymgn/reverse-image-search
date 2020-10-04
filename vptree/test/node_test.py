import unittest

from vptree.node import VPTreeNode

NODE_CAPACITY = 32


def dist_fn(x, y):
    return abs(x - y)


def create_test_nodes():
    points = [i for i in range(NODE_CAPACITY)]

    test_nodes = [
        VPTreeNode(points, dist_fn, len(points) * 2),
        VPTreeNode(points, dist_fn, len(points)),
        VPTreeNode(points, dist_fn, len(points) // 8),
    ]

    return test_nodes


class TestVPTreeNode(unittest.TestCase):
    def test_size(self):
        nodes = create_test_nodes()
        for node in nodes:
            self.assertEqual(NODE_CAPACITY, node.size())

    def test_add(self):
        nodes = create_test_nodes()
        test_point = NODE_CAPACITY * 2
        for node in nodes:
            self.assertFalse(node.contains(test_point))
            node.add(test_point)
            self.assertEqual(NODE_CAPACITY + 1, node.size())
            self.assertTrue(node.contains(test_point))

    def test_contains(self):
        nodes = create_test_nodes()
        point_not_in_node = NODE_CAPACITY * 2
        for node in nodes:
            for i in range(NODE_CAPACITY):
                self.assertTrue(node.contains(i))
            self.assertFalse(node.contains(point_not_in_node))

    def test_remove(self):
        nodes = create_test_nodes()
        point_in_node = NODE_CAPACITY // 2
        point_not_in_node = NODE_CAPACITY * 2
        for node in nodes:
            self.assertFalse(node.remove(point_not_in_node))
            self.assertTrue(node.remove(point_in_node))

            self.assertEqual(NODE_CAPACITY - 1, node.size())

            for i in range(NODE_CAPACITY):
                node.remove(i)

            self.assertEqual(0, node.size())

    def test_get_nearest_neighbours(self):
        nodes = create_test_nodes()
        query = NODE_CAPACITY // 2
        num_neighbours = 3
        for node in nodes:
            res = node.get_nearest_neighbours(query, num_neighbours, num_neighbours)
            self.assertEqual(len(res), num_neighbours)
            self.assertEqual(query, res[0])
            for v in [query - 1, query, query + 1]:
                self.assertIn(v, res)

    def test_get_within_distance(self):
        nodes = create_test_nodes()
        query = NODE_CAPACITY // 2
        max_distance = NODE_CAPACITY // 8
        for node in nodes:
            res = node.get_within_distance(query, max_distance)
            self.assertEqual(2 * max_distance + 1, len(res))
            for i in range(query - max_distance, query + max_distance + 1):
                self.assertIn(i, res)


if __name__ == '__main__':
    unittest.main()
