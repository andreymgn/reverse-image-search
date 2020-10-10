import pickle
from typing import List

from image.image import Image
from vptree.vptree import VPTree


class DB:
    def __init__(self, tree: VPTree, images: List[Image], hash_type, hash_size):
        self.tree = tree
        self.image_hashes = {img.path: img.hash for img in images}
        self.images = set(images)
        self.hash_type = hash_type
        self.hash_size = hash_size

    def encode(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f)


def decode(path) -> DB:
    with open(path, 'rb') as f:
        return pickle.load(f)
