import functools
import os
from multiprocessing import Pool as ThreadPool
from typing import Dict, List, Callable

from db.db import DB, decode
from image import image
from vptree.vptree import VPTree

DEFAULT_HASH_TYPE = 'dhash'
DEFAULT_HASH_SIZE = 8


def walkdir(parent_dir: str, recursive: bool, path_func: Callable[[str], None]):
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
    walkdir(args.dir, args.recursive, lambda path: init_func(path, tree, files, args.hash_type, args.hash_size))
    db = DB(tree, files, args.hash_type, args.hash_size)
    db.encode(args.db)


def init_func(path, tree: VPTree, files: List[image.Image], hash_type=DEFAULT_HASH_TYPE, hash_size=DEFAULT_HASH_SIZE):
    try:
        img = image.Image(path, hash_type, hash_size)
        tree.add(img)
        files.append(img)
    except OSError as e:
        print('Exception adding file {}. Reason: {}'.format(path, e))


def add(args):
    db = decode(args.db)
    img = image.Image(args.image, db.hash_type, db.hash_size)
    db.tree.add(img)
    db.image_hashes.add(args.image)
    db.encode(args.db)


def update(args):
    db = decode(args.db)
    walkdir(args.dir, args.recursive,
            lambda path: update_func(path, db.tree, db.image_hashes, db.hash_type, db.hash_size))
    db.encode(args.db)


def update_func(path: str, tree: VPTree, files: Dict[str, int], hash_type=DEFAULT_HASH_TYPE,
                hash_size=DEFAULT_HASH_SIZE):
    if path not in files:
        try:
            img = image.Image(path, hash_type, hash_size)
            tree.add(img)
            files[img.path] = img.hash
        except OSError as e:
            print('Exception adding file {}. Reason: {}'.format(path, e))


def search_by_distance(args):
    db = decode(args.db)
    query = image.Image(args.query, db.hash_type, db.hash_size)
    out = db.tree.get_within_distance(query, args.max_distance)

    if len(out) == 0:
        return
    for img in out:
        if os.path.abspath(args.query) == img.path:
            continue
        print('path {} distance: {}'.format(img.path, query.distance(img)))


def search_nearest(args):
    db = decode(args.db)
    query = image.Image(args.query, db.hash_type, db.hash_size)
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
    img = image.Image(path, db.hash_type, db.hash_size)

    if path in db.image_hashes:
        if db.tree.remove(img):
            del db.image_hashes[path]
            db.encode(args.db)
        else:
            raise ValueError('path is in dict but not in tree')


def rebuild(args):
    db = decode(args.db)
    hash_size = args.hash_size if args.hash_size != 0 else db.hash_size
    hash_type = args.hash_type if len(args.hash_type) != 0 else db.hash_type

    imgs = []
    files = []

    for path in db.image_hashes:
        img = image.Image(path, hash_type, hash_size)
        imgs.append(img)
        files.append(img)

    tree = VPTree(distance_fn=image.distance_fn)
    tree.add_list(imgs)
    db = DB(tree, files, hash_type, hash_size)
    db.encode(args.db)


def clusters(args):
    db = decode(args.db)

    imgs = list(db.images)
    batches = imgs if args.num_threads == 1 else _split(imgs, args.num_threads)

    pool = ThreadPool(args.num_threads)
    batch_clusters = pool.map(functools.partial(_get_neighbours, db.tree, args.num_neighbours, args.min_distance),
                              batches)
    pool.close()
    pool.join()

    clusters_list = [item for sublist in batch_clusters for item in sublist]

    clusters = {}
    for i in range(0, len(imgs)):
        if len(clusters_list[i]) != 0:
            clusters[imgs[i].path] = clusters_list[i]

    for img_path, nearest in clusters.items():
        print('image: {}'.format(img_path))
        print('\tpath\tdistance')
        for n in nearest:
            print('\t{}\t{}'.format(n[0], n[1]))
        print()


def _get_neighbours(tree: VPTree, num_neighbours: int, min_distance: int, img_batch: List[image.Image]):
    result = []
    for img in img_batch:
        neighbours = tree.get_nearest_neighbours(img, num_neighbours)
        l = []
        for n in neighbours:
            dist = img.distance(n)
            if n.path == img.path or dist > min_distance:
                continue
            l.append((n.path, dist))

        result.append(l)

    return result


def _split(seq: List, num_chunks: int):
    avg = len(seq) / float(num_chunks)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out
