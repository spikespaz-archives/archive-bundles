#! /usr/bin/python3

import re
from urllib import request


class HostsManager:
    def __init__(self, **kwargs):
        self.sources = kwargs.get("sources", [
            "https://adaway.org/hosts.txt", "https://hosts-file.net/ad_servers.txt",
            "https://pgl.yoyo.org/adservers/serverlist.php?hostformat=hosts&showintro=0&mimetype=plaintext"
        ])
        self.host_ipv4 = kwargs.get("host_ipv4", "127.0.0.2")
        self.host_ipv6 = kwargs.get("host_ipv6", "::1")
        self.whitelist = kwargs.get("whitelist", [])
        self.blacklist = kwargs.get("blacklist", [])
        self.redirects = kwargs.get("redirects", [])

    def fetch(self):
        host_domains = set()

        for source_url in self.sources:
            source_request = request.Request(source_url, headers={"User-Agent": self.__class__.__name__})
            source_response = request.urlopen(source_request)

            for host_line in source_response:
                host_line = host_line.strip()

                if host_line and not host_line.startswith(b"#"):
                    host_domains.add(self.parse_line(host_line.decode()))

        return host_domains

    def merge(self):
        host_domains = self.fetch()

        for host_domain in self.whitelist:
            host_domains.discard(host_domain)

        for host_domain in self.blacklist:
            host_domains.add(host_domain)

        return host_domains

    def build(self):
        host_domains = self.merge()
        host_list = []
        host_length = len(max(self.host_ipv4, self.host_ipv6,
                          *map(lambda redirect: redirect[0], self.redirects), key=len)) + 2

        for host_domain in host_domains:
            host_list.append(self.host_ipv4.ljust(host_length) + host_domain)
            host_list.append(self.host_ipv6.ljust(host_length) + host_domain)

        for redirect in self.redirects:
            host_list.append(redirect[0].ljust(host_length) + redirect[1])

        return host_list

    @staticmethod
    def parse_line(host_line):
        return re.split(r"\s+", host_line, 2)[1]
