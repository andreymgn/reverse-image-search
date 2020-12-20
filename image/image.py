import imagehash
from PIL import Image as PILImage
from imagehash import ImageHash


def _get_hash(image_path: str, hash_type: str, hash_size: int = 8) -> imagehash.ImageHash:
    hash_strs = {
        'phash': imagehash.phash,
        'dhash': imagehash.dhash,
        'ahash': imagehash.average_hash,
        'whash': imagehash.whash
    }
    if hash_type not in hash_strs:
        raise ValueError('invalid hash type {}'.format(hash_type))
    img = PILImage.open(image_path)
    return hash_strs[hash_type](img, hash_size)


class Image:
    hash: ImageHash
    path: str

    def __init__(self, path: str, hash_type: str, hash_size: int = 8):
        self.path = path
        self.hash = _get_hash(path, hash_type, hash_size)

    def distance(self, other: 'Image') -> float:
        return self.hash - other.hash

    def __lt__(self, other: 'Image') -> bool:
        return self.path < other.path

    def __eq__(self, other: 'Image') -> bool:
        return self.path == other.path and self.hash == other.hash

    def __hash__(self) -> int:
        return hash((self.path, self.hash))


def distance_fn(im1: Image, im2: Image) -> float:
    return im1.distance(im2)
