#! /usr/bin/env python3

import os

hosts_header = """
# Copyright (c) 1993-2009 Microsoft Corp.
#
# This is a sample HOSTS file used by Microsoft TCP/IP for Windows.
#
# This file contains the mappings of IP addresses to host names. Each
# entry should be kept on an individual line. The IP address should
# be placed in the first column followed by the corresponding host name.
# The IP address and the host name should be separated by at least one
# space.
#
# Additionally, comments (such as these) may be inserted on individual
# lines or following the machine name denoted by a '#' symbol.
#
# For example:
#
#      102.54.94.97     rhino.acme.com          # source server
#       38.25.63.10     x.acme.com              # x client host
# localhost name resolution is handled within DNS itself.
#       127.0.0.1       localhost
#       ::1             localhost
"""

# hosts_path = os.environ["SYSTEMROOT"] + r"\System32\Drivers\etc\hosts"
hosts_path = r".\hosts"


def read():
    with open(hosts_path, "r") as hosts_file:
        hosts_list = []

        for host_line in hosts_file.readlines():
            host_line = host_line.strip()

            if host_line and not host_line.startswith("#"):
                hosts_list.append(host_line.split(" ", 1)[1].split("#", 1)[0].strip())

        return hosts_list


def write(in_list, redirect="0.0.0.0"):
    with open(hosts_path, "a") as hosts_file:
        hosts_file.seek(0)
        hosts_file.truncate()

        hosts_file.write(hosts_header)

        for host in in_list:
            hosts_file.write(redirect + " " + host.strip() + "\n")


write(["test.com", "test2.com"])
