#!/usr/bin/env python3

"""
This script parses the `!include` directive in YAML files.
"""
import os
import sys
import json
import yaml
import pathlib
import argparse

from typing import Any, IO


class Loader(yaml.SafeLoader):
    """YAML Loader with `!include` constructor."""

    def __init__(self, stream: IO) -> None:
        """Initialise Loader."""
        try:
            self._root = os.path.split(stream.name)[0]
        except AttributeError:
            self._root = os.path.curdir

        super().__init__(stream)

def construct_include(loader: Loader, node: yaml.Node) -> Any:
    """Include file referenced at node."""

    filename = os.path.abspath(os.path.join(loader._root, loader.construct_scalar(node)))
    extension = os.path.splitext(filename)[1].lstrip('.')

    with open(filename, 'r') as f:
        if extension in ('yaml', 'yml'):
            return yaml.load(f, Loader)
        elif extension in ('json', ):
            return json.load(f)
        else:
            return ''.join(f.readlines())

yaml.add_constructor('!include', construct_include, Loader)


def main():
    parser = argparse.ArgumentParser(description="Custom parser for YAML files")
    parser.add_argument("file", type=argparse.FileType('r'), help='path to yaml file')
    args = parser.parse_args()
    
    try:
        # Generate python object from input YAML
        parsed_yaml = yaml.load(args.file, Loader)
        # Print parsed YAML
        print(yaml.dump(parsed_yaml))
    except FileNotFoundError as err:
        print(f"{parser.prog}: {args.file.name}: {err}", file=sys.stderr)

if __name__ == "__main__":
    main()