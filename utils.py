#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QFileDialog
from glob import glob

import errno
import os
import sys

ERROR_INVALID_NAME = 123


# From https://stackoverflow.com/a/34102855 - Question #1
def is_path_exists(pathname: str) -> bool:
    """`True` if the passed pathname is a valid pathname for the current OS;
    `False` otherwise.
    """
    try:
        if not isinstance(pathname, str) or not pathname:
            return False

        _, pathname = os.path.splitdrive(pathname)

        root_dirname = os.environ.get("HOMEDRIVE", "C:") \
            if sys.platform == "win32" else os.path.sep
        assert os.path.isdir(root_dirname)

        root_dirname = root_dirname.rstrip(os.path.sep) + os.path.sep

        for pathname_part in pathname.split(os.path.sep):
            try:
                os.lstat(root_dirname + pathname_part)
            except OSError as exc:
                if hasattr(exc, "winerror"):
                    if exc.winerror == ERROR_INVALID_NAME:
                        return False
                elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                    return False
    except TypeError as exc:
        return False
    else:
        return True


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


def glob_from(path, ext):
    """Return glob from a directory."""
    working_dir = os.getcwd()
    os.chdir(path)

    file_paths = glob("**/*." + ext)

    os.chdir(working_dir)

    return file_paths