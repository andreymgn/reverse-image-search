from PIL import Image as PILImage
import numpy as np


def _dhash(img: PILImage.Image):
    img = img.convert("L").resize((9, 8), PILImage.ANTIALIAS)
    pixels = np.asarray(img)
    diff = pixels[:, 1:] > pixels[:, :-1]
    return sum([2 ** (i % 8) for i, v in enumerate(diff.flatten()) if v])


def _get_hash(image_path):
    img = PILImage.open(image_path)
    return _dhash(img)


class Image:
    def __init__(self, path):
        self.path = path
        self.hash = _get_hash(path)

    def distance(self, other: 'Image'):
        return bin(self.hash ^ other.hash).count('1')
