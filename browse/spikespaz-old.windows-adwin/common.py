#! /usr/bin/env python3


def str_to_list(in_str):
    return [line for line in list(map(str.strip, in_str.split("\n"))) if line]


def list_to_str(in_list):
    return "\n".join([line for line in in_list if line])
