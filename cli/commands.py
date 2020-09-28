import os

from image import image
from vptree.vptree import VPTree, encode, decode


def walkdir(tree, parent_dir):
    for (dirpath, dirnames, filenames) in os.walk(parent_dir):
        for f in filenames:
            print(os.path.join(dirpath, f))
            img = image.Image(os.path.join(dirpath, f))
            tree.add(img)
        for directory in dirnames:
            walkdir(tree, directory)


def init(args):
    tree = VPTree(distance_fn=image.distance_fn)
    walkdir(tree, args.dir)
    encode(tree, args.db)


def add(args):
    tree = decode(args.db)
    img = image.Image(args.image)
    tree.add(img)
    encode(tree, args.db)
