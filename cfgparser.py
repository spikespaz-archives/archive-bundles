#! /usr/bin/env python3
"""Small reader and writer for shell-esque configurations strings or files."""

from ast import literal_eval


class RawString(str):
    """Wrapper around the `str` class to specify that it is a raw string."""

    def __repr__(self):
        return "\"" + self + "\""


def _reads(string):
    """Read a configuration string. Returns a list of (key, value) pairs."""
    content = []

    for line in string.strip().splitlines():
        line = line.split("=", 1)
        line = [line[0].strip(), line[1].strip()]

        if line[1].lower() in ("", "none"):
            line[1] = None
        elif line[1].startswith("'") and line[1].endswith("'"):
            line[1] = RawString(literal_eval(line[1]))
        else:
            try:
                line[1] = literal_eval(line[1])
            except ValueError:
                pass

        content.append(line)

    return content


def reads(string):
    """Read a configuration string. Returns a dictionary."""
    return dict(_reads(string))


def read(file_path):
    """Read a configuration file. Returns a dictionary."""
    with open(file_path, "r") as config_file:
        return reads(config_file.read())


def dumps(config, padding=0):
    """Dump a configuration dictionary to a string."""
    content = ""

    for (key, value) in config.items():
        if value is None:
            value = ""
        elif type(value) is RawString:
            value = "'" + str(value) + "'"
        else:
            value = repr(value)

            if value.startswith("'") and value.endswith("'"):
                value = "\"" + value[1:-1] + "\""

        content += "{key}{padding}={padding}{value}\n".format(key=str(key).strip(),
                                                              value=value,
                                                              padding=" " * padding)

    return content


def dump(config, file_path, padding=0):
    """Dump a configuration dictionary to a file."""
    with open(file_path, "w") as config_file:
        config_file.write(dumps(config, padding))
