import argparse
import os

import cli.commands

parser = argparse.ArgumentParser(description='imdex - local image index')
parser.add_argument('--db', default='imdex.db')

subparsers = parser.add_subparsers()
parser_init = subparsers.add_parser('init', help='initialize imdex')
parser_init.add_argument('--dir', default=os.curdir, help='directory to scan for images')
parser_init.add_argument('--recursive', '-r', default=True, help='build recursively')
parser_init.set_defaults(func=cli.commands.init)

parser_add = subparsers.add_parser('add', help='add new image to imdex')
parser_add.add_argument('--image', required=True, help='path to image')
parser_add.set_defaults(func=cli.commands.add)

parser_update = subparsers.add_parser('update', help='scan directory and add new images')
parser_update.add_argument('--dir', default=os.curdir, help='directory to scan for images')
parser_update.add_argument('--recursive', '-r', default=True, help='update recursively')
parser_update.set_defaults(func=cli.commands.update)

args = parser.parse_args()
if 'func' in args:
    print(args)
    args.func(args)
else:
    print(args)
    parser.print_usage()
