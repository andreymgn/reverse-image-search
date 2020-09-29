import pickle
from typing import List

from vptree.vptree import VPTree


class DB:
    def __init__(self, tree: VPTree, image_paths: List[str]):
        self.tree = tree
        self.image_paths = set(image_paths)

    def encode(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f)


def decode(path) -> DB:
    with open(path, 'rb') as f:
        return pickle.load(f)
