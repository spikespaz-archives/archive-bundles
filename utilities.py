#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import errno

from glob import glob
from functools import wraps
from contextlib import contextmanager
from PyQt5.QtWidgets import QFileDialog


#: Constant for the invalid path name OS error code.
ERROR_INVALID_NAME = 123


# From https://stackoverflow.com/a/34102855 - Question #1
def path_valid(pathname):
    """`True` if the passed pathname is a valid pathname for the current OS; `False` otherwise."""
    try:
        if not isinstance(pathname, str) or not pathname:
            return False

        _, pathname = os.path.splitdrive(pathname)

        root_dir = os.environ.get("HOMEDRIVE", "C:") \
            if sys.platform == "win32" else os.path.sep
        assert os.path.isdir(root_dir)

        root_dir = root_dir.rstrip(os.path.sep) + os.path.sep

        for pathname_part in pathname.split(os.path.sep):
            try:
                os.lstat(root_dir + pathname_part)
            except OSError as exc:
                if hasattr(exc, "winerror"):
                    if exc.winerror == ERROR_INVALID_NAME:
                        return False
                elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                    return False
    except TypeError as _:
        return False
    else:
        return True


# From https://stackoverflow.com/a/34102855 - Question #2
def path_creatable(pathname):
    """`True` if the current user has sufficient permissions to create the passed pathname; `False` otherwise."""
    dir_name = os.path.dirname(pathname) or os.getcwd()
    return os.access(dir_name, os.W_OK)


# From https://stackoverflow.com/a/34102855 - Question #2
def path_exists_or_creatable(pathname):
    """`True` if the passed pathname is a valid pathname for the current OS _and_ either currently exists
    or is hypothetically creatable; `False` otherwise.

    This function is guaranteed to _never_ raise exceptions.
    """
    try:
        return path_valid(pathname) and (
            os.path.exists(pathname) or path_creatable(pathname))
    except OSError:
        return False


def open_directory_picker(parent, path="", title="Select Directory", native=True):
    """Opens a directory selection dialogue based on the parent window at the specified path.
    If the path specified is blank (default) just use the current directory."""
    picker = QFileDialog()
    picker.setDirectory(path)

    if native:
        return str(picker.getExistingDirectory(parent, title))
    else:
        return str(picker.getExistingDirectory(parent, title, options=QFileDialog.DontUseNativeDialog))


def set_combo(combo, string):
    """Set a `QtWidgets.QComboBox` index by a matching string value."""
    if string:
        items = [combo.itemText(item).lower() for item in range(combo.count())]
        combo.setCurrentIndex(items.index(string.lower()))


def glob_from(path, pattern):
    """Return glob from a directory."""
    with chdir(path):
        return glob(pattern)


def replace_base(input_dir, output_dir, input_path):
    """Replace the base directory path relative to an input directory and replace it with another directory path."""
    return os.path.join(output_dir, os.path.relpath(input_dir, input_path))


def replace_ext(path, ext):
    """Replace the extension of a path."""
    return os.path.splitext(path)[1] + "." + ext.lower()


@contextmanager
def chdir(*args, **kwargs):
    """Context manager for acting within a new working directory temporarily."""
    working_dir = os.getcwd()
    os.chdir(*args, **kwargs)

    try:
        yield os.getcwd()
    finally:
        os.chdir(working_dir)


def str_matches(string, *matches):
    """Return `True` if the lowercase version of a string matches any of the following lowercase strings."""
    if not isinstance(string, str):
        return False

    return string.lower() in (match.lower() for match in matches)


def unzip_args(func):
    """Wrapper to make args and kwargs passable to map."""
    @wraps(func)
    def wrapper(args_kwargs):
        args, kwargs = args_kwargs
        return func(*args, **kwargs)
    return wrapper


def clamp(value, minimum=0, maximum=1):
    """Return a numeral clamped between a min and a max value."""
    return sorted((minimum, value, maximum))[1]


def _pass(self, *args, **kwargs):
    """Do nothing."""
    pass
