import os
from typing import Dict

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
    files.append(img)


def add(args):
    db = decode(args.db)
    img = image.Image(args.image)
    db.tree.add(img)
    db.image_hashes.add(args.image)
    db.encode(args.db)


def update(args):
    db = decode(args.db)
    walkdir(args.dir, args.recursive, lambda path: update_func(path, db.tree, db.image_hashes))
    db.encode(args.db)


def update_func(path, tree, files: Dict[str, int]):
    if path not in files:
        img = image.Image(path)
        tree.add(img)
        files[img.path] = img.hash


def search_by_distance(args):
    db = decode(args.db)
    query = image.Image(args.query)
    out = db.tree.get_within_distance(query, args.max_distance)
    if len(out) == 0:
        return
    for img in out:
        if os.path.abspath(args.query) == img.path:
            continue
        print('path {} distance: {}'.format(img.path, query.distance(img)))


def search_nearest(args):
    db = decode(args.db)
    query = image.Image(args.query)
    out = db.tree.get_nearest_neighbours(query, args.num_neighbours, args.max_results)
    if len(out) == 0:
        return
    for img in out:
        if os.path.abspath(args.query) == img.path:
            continue
        print('path {} distance: {}'.format(img.path, query.distance(img)))


def remove(args):
    db = decode(args.db)
    path = os.path.abspath(args.image)
    img = image.Image(path)
    if path in db.image_hashes:
        if db.tree.remove(img):
            del db.image_hashes[path]
            db.encode(args.db)
        else:
            raise ValueError('path is in dict but not in tree')