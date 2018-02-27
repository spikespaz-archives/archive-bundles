#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from os import system
from pyquery import PyQuery
from platform import machine
from urllib.request import urlretrieve
from tempfile import TemporaryDirectory
from utilities import Reporter, WithDir, ChainedContext

ITUNES_URL = "https://www.apple.com/itunes/download/"
LINK_SELECTOR = "div.download>a.button.button-download"

print("Getting iTunes document...")
document = PyQuery(url=ITUNES_URL)

print("Getting download URLs...")
download_urls = [anchor.attrib["href"] for anchor in document(LINK_SELECTOR)]

print("Determining machine architecture...")
architecture = "64" if machine() == "AMD64" else ""

with ChainedContext(TemporaryDirectory, WithDir):
    print("Downloading iTunes installer...")
    urlretrieve(download_urls[1] if architecture else download_urls[0],
                filename="iTunesSetup.exe", reporthook=Reporter())
    print()

    print("Extracting iTunes install files...")
    system("iTunesSetup.exe /extract")

    print("Starting Bonjour installer...")
    system("Bonjour" + architecture + ".msi")
