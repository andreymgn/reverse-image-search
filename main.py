import argparse
import os

import cli.commands

parser = argparse.ArgumentParser(description='imdex - local image index')
parser.add_argument('--db', default='imdex.db')

subparsers = parser.add_subparsers()
parser_init = subparsers.add_parser('init', help='initialize imdex')
parser_init.add_argument('--dir', default=os.curdir)
parser_init.set_defaults(func=cli.commands.init)

parser_add = subparsers.add_parser('add', help='add new image to imdex')
parser_add.add_argument('--image', required=True)
parser_add.set_defaults(func=cli.commands.add)

args = parser.parse_args()
if 'func' in args:
    args.func(args)
else:
    parser.print_usage()
