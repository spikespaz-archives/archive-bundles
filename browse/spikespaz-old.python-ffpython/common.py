#! /usr/bin/env python3
from os import path, mkdir


def mkfpath(file_path):
    """Make the path up to a file if it doesn't already exist."""
    base_path = path.dirname(file_path)

    if not path.isdir:
        mkdir(base_path)
