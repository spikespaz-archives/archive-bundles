#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QFileDialog
from pathlib import Path

import os


# Replaces the function previously found at SO. THis is simpler and uses python built-ins.
def is_path_exists(path):
    """Return `True` if a path exists, `False` otherwise."""
    return Path(path).exists()


# From https://stackoverflow.com/a/34102855 - Question #2
def is_path_creatable(pathname: str) -> bool:
    """`True` if the current user has sufficient permissions to create the passed
    pathname; `False` otherwise.
    """
    dirname = os.path.dirname(pathname) or os.getcwd()
    return os.access(dirname, os.W_OK)


# From https://stackoverflow.com/a/34102855 - Question #2
def is_path_exists_or_creatable(pathname: str) -> bool:
    """`True` if the passed pathname is a valid pathname for the current OS _and_
    either currently exists or is hypothetically creatable; `False` otherwise.

    This function is guaranteed to _never_ raise exceptions.
    """
    try:
        return is_path_exists(pathname) and (
            os.path.exists(pathname) or is_path_creatable(pathname))
    except OSError:
        return False


def open_directory_picker(parent, path=""):
    """Opens a directory selection dialogue based on the parent window at the specified path.
    If the path specified is blank (default) just use the current directory."""
    picker = QFileDialog()
    picker.setDirectory(path)

    return str(picker.getExistingDirectory(parent, "Select Directory"))


def file_batch_operation(input_dir, output_dir, extension, operation):
    """A function to run a function on each file in a directory tree, and mirror that tree somewhere else."""
    path_list = Path(input_dir).glob("**/*." + extension)
    path_list = [(path, str(path).replace(input_dir, output_dir)) for path in path_list]

    for path in path_list:
        if path[0].is_file():
            os.makedirs(path[1], exist_ok=True)
            yield operation(str(path[0], path[1]))
