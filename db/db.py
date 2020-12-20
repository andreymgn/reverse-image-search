import pickle
from typing import List, Dict, Set

import imagehash

from image.image import Image
from vptree.vptree import VPTree


class DB:
    hash_size: int
    hash_type: str
    images: Set[Image]
    image_hashes: Dict[str, imagehash.ImageHash]
    tree: VPTree

    def __init__(self, tree: VPTree, images: List[Image], hash_type: str, hash_size: int):
        self.tree = tree
        self.image_hashes = {img.path: img.hash for img in images}
        self.images = set(images)
        self.hash_type = hash_type
        self.hash_size = hash_size

    def encode(self, path: str):
        with open(path, 'wb') as f:
            pickle.dump(self, f)


def decode(path: str) -> DB:
    with open(path, 'rb') as f:
        return pickle.load(f)
