#! /usr/bin/env python3


def str_to_list(in_str):
    return list(map(str.strip, in_str.split("\n")))


def list_to_str(in_list):
    return "\n".join(in_list)
