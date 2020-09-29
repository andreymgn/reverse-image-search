import os

from db.db import DB, decode
from image import image
from vptree.vptree import VPTree


def walkdir(parent_dir, recursive, path_func):
    for (dirpath, dirnames, filenames) in os.walk(parent_dir):
        for f in filenames:
            path = os.path.abspath(os.path.join(dirpath, f))
            path_func(path)
        if recursive:
            for directory in dirnames:
                walkdir(directory, recursive, path_func)


def init(args):
    tree = VPTree(distance_fn=image.distance_fn)
    files = []
    walkdir(args.dir, args.recursive, lambda path: init_func(path, tree, files))
    db = DB(tree, files)
    db.encode(args.db)


def init_func(path, tree, files):
    img = image.Image(path)
    tree.add(img)
    files.append(path)


def add(args):
    db = decode(args.db)
    img = image.Image(args.image)
    db.tree.add(img)
    db.image_paths.add(args.image)
    db.encode(args.db)


def update(args):
    db = decode(args.db)
    walkdir(args.dir, args.recursive, lambda path: update_func(path, db.tree, db.image_paths))
    db.encode(args.db)


def update_func(path, tree, files):
    if path not in files:
        img = image.Image(path)
        tree.add(img)
        files.add(path)
