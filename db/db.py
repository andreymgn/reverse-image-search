import pickle
from typing import List

from image.image import Image
from vptree.vptree import VPTree


class DB:
    def __init__(self, tree: VPTree, images: List[Image]):
        self.tree = tree
        self.image_hashes = {img.path: img.hash for img in images}

    def encode(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f)


def decode(path) -> DB:
    with open(path, 'rb') as f:
        return pickle.load(f)
