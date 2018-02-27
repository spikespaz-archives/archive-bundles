#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from pyquery import PyQuery
from platform import machine
from os import system, chdir, getcwd
from urllib.request import urlretrieve
from tempfile import TemporaryDirectory


class WithDir:
    def __init__(self, work_dir):
        self.work_dir = work_dir

    def __enter__(self):
        self.real_dir = getcwd()
        chdir(self.work_dir)
        return self.work_dir

    def __exit__(self, *_):
        chdir(self.real_dir)
        del self.real_dir


ITUNES_URL = "https://www.apple.com/itunes/download/"
LINK_SELECTOR = "div.download>a.button.button-download"


print("Getting iTunes document...")
document = PyQuery(url=ITUNES_URL)

print("Getting download URLs...")
download_urls = [anchor.attrib["href"] for anchor in document(LINK_SELECTOR)]
_, download_32, download_64 = download_urls

print("Determining machine architecture...")
architecture = "64" if machine() == "AMD64" else ""

download_url = download_64 if architecture else download_32
print("Download URL:", download_url)

with TemporaryDirectory() as extract_path:
    with WithDir(extract_path):
        print("Downloading iTunes installer...")
        urlretrieve(download_url, filename="iTunesSetup.exe")
        print()

        print("Extracting iTunes install files...")
        system("iTunesSetup.exe /extract")

        print("Starting Bonjour installer...")
        system("Bonjour" + architecture + ".msi")
