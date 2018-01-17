#! /usr/bin/env python3
from setuptools import setup, find_packages

PROJECT = {
    "name": "quizlet.py",
    "version": "0.0.1",
    "description": "A pythonic wrapper for the official Quizlet API 2.0.",
    "long_description": None,
    "url": "https://github.com/spikespaz.quizlet.py",
    "author": "spikespaz",
    "author_email": "spikespaz@outlook.com",
    "classifiers": [
        "Development Status :: 2 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English"
        "Operating System :: OS Independent"
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Topic :: Utilities",
        "Topic :: Games/Entertainment",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    "keywords": "development api quizlet wrapper library rest game vocabulary",
    "packages": find_packages(exclude=["docs"])
}

setup(**PROJECT)
