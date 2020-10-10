import argparse
import multiprocessing
import os

import cli.commands

parser = argparse.ArgumentParser(description='imdex - local image index')
parser.add_argument('--db', default='imdex.db')

subparsers = parser.add_subparsers()
parser_init = subparsers.add_parser('init', help='initialize imdex')
parser_init.add_argument('--dir', default=os.curdir, help='directory to scan for images')
parser_init.add_argument('--recursive', '-r', default=True, help='build recursively')
parser_init.add_argument('--hash_type', default='dhash', type=str, help='hash type')
parser_init.add_argument('--hash_size', default=8, type=int, help='hash size')
parser_init.set_defaults(func=cli.commands.init)

parser_add = subparsers.add_parser('add', help='add new image to imdex')
parser_add.add_argument('image', metavar='image', help='path to image')
parser_add.set_defaults(func=cli.commands.add)

parser_update = subparsers.add_parser('update', help='scan directory and add new images')
parser_update.add_argument('--dir', default=os.curdir, help='directory to scan for images')
parser_update.add_argument('--recursive', '-r', default=True, help='update recursively')
parser_update.set_defaults(func=cli.commands.update)

parser_search = subparsers.add_parser('search', help='search for similar images')
parser_search.add_argument('query', metavar='query', help='query image')
parser_search.add_argument('--max_distance', default=3, type=int)
parser_search.set_defaults(func=cli.commands.search_by_distance)

parser_nearest = subparsers.add_parser('nearest', help='get nearest images')
parser_nearest.add_argument('query', metavar='query', help='query image')
parser_nearest.add_argument('--max_results', default=16, type=int)
parser_nearest.add_argument('--num_neighbours', default=3, type=int)
parser_nearest.set_defaults(func=cli.commands.search_nearest)

parser_remove = subparsers.add_parser('remove', help='remove image from imdex')
parser_remove.add_argument('image', metavar='image', help='path to image')
parser_remove.set_defaults(func=cli.commands.remove)

parser_rebuild = subparsers.add_parser('rebuild', help='rebuild imdex')
parser_rebuild.add_argument('--hash_type', default='', type=str, help='hash type')
parser_rebuild.add_argument('--hash_size', default=0, type=int, help='hash size')
parser_rebuild.set_defaults(func=cli.commands.rebuild)

parser_clusters = subparsers.add_parser('clusters', help='show image clusters')
parser_clusters.add_argument('--num_neighbours', default=3)
parser_clusters.add_argument('--min_distance', default=2)
parser_clusters.add_argument('--num_threads', default=multiprocessing.cpu_count(), type=int)
parser_clusters.set_defaults(func=cli.commands.clusters)

args = parser.parse_args()
if 'func' in args:
    args.func(args)
else:
    parser.print_usage()
