#!/usr/bin/env python3
import contextlib
import functools
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib import parse


@contextlib.contextmanager
def work_directory(path):
    try:
        cwd = os.getcwd()
        os.chdir(path)
        yield Path(path)
    finally:
        os.chdir(cwd)


def is_dir_empty(path):
    path = Path(path)
    if path.exists():
        try:
            next(path.iterdir())
            return False
        except StopIteration:
            return True


class Repository:
    def __init__(self, url):
        self.url = url

    @property
    @functools.cache
    def author(self):
        return self.fullname.split("/")[0]

    @property
    @functools.cache
    def name(self):
        return self.fullname.split("/")[1]

    @property
    @functools.cache
    def fullname(self):
        return "/".join(parse.urlparse(self.url).path.rsplit("/", 2)[1:])


class Bundle:
    def __init__(self, repo, browse_parent_dir, bundle_parent_dir):
        self.repo = repo
        self._browse_parent_dir = browse_parent_dir
        self._bundle_parent_dir = bundle_parent_dir

    @property
    def _browse_parent_dir(self):
        return self.__browse_parent_dir

    @_browse_parent_dir.setter
    def _browse_parent_dir(self, path):
        self.__browse_parent_dir = Path(path)

    @property
    def _bundle_parent_dir(self):
        return self.__bundle_parent_dir

    @_bundle_parent_dir.setter
    def _bundle_parent_dir(self, path):
        self.__bundle_parent_dir = Path(path)

    @property
    @functools.cache
    def name(self):
        return "{}.{}".format(self.repo.author, self.repo.name)

    @property
    @functools.cache
    def browse_path(self):
        return self._browse_parent_dir / self.repo.fullname

    @property
    @functools.cache
    def bundle_path(self):
        return (self._bundle_parent_dir / (self.name + ".bundle"))


def parse_repo_list(file_path):
    with open(file_path) as file:
        for line in file.readlines():
            line = line.strip()
            if not len(line):
                continue

            yield Repository(line)


def clone_repo(repo_url, clone_path, stdout=sys.stderr, stderr=sys.stderr):
    return subprocess.run(
        subprocess.list2cmdline(("git", "clone", repo_url, clone_path)),
        stdout=stdout,
        stderr=stderr,
        shell=True
    ).returncode == 0


def bundle_repo(repo_path, dest_file, stdout=sys.stderr, stderr=sys.stderr):
    return subprocess.run(
        subprocess.list2cmdline(
            ("git", "bundle", "create", dest_file, "--all")),
        stdout=stdout,
        stderr=stderr,
        shell=True,
        cwd=repo_path
    ).returncode == 0


def main(repo_list_file, repo_browse_dir, repo_bundle_dir):
    repo_list_file = Path(repo_list_file)
    repo_browse_dir = Path(repo_browse_dir)
    repo_bundle_dir = Path(repo_bundle_dir)

    print("INFO: Parsing repository list file...")
    repo_list = set(parse_repo_list(repo_list_file))

    invalid_dirs = set()
    invalid_files = set()

    if repo_browse_dir.is_file():
        invalid_dirs.add(repo_browse_dir)
    else:
        repo_browse_dir.mkdir(parents=True, exist_ok=True)

    if repo_bundle_dir.is_file():
        invalid_dirs.add(repo_bundle_dir)
    else:
        repo_bundle_dir.mkdir(parents=True, exist_ok=True)

    repo_browse_dir = repo_browse_dir.resolve()
    repo_bundle_dir = repo_bundle_dir.resolve()

    bundle_list = tuple(
        Bundle(repo, repo_browse_dir, repo_bundle_dir) for repo in repo_list)

    browse_paths_exist = set()
    browse_paths_no_exist = set()
    browse_paths_are_empty = set()
    bundle_paths_exist = set()
    bundle_paths_no_exist = set()
    browse_parent_dirs = set()

    for bundle in bundle_list:
        if bundle.browse_path.is_file():
            invalid_files.add(bundle.browse_path)
        elif bundle.browse_path.is_dir():
            if is_dir_empty(bundle.browse_path):
                browse_paths_are_empty.add(bundle)
            else:
                browse_paths_exist.add(bundle)
        else:
            browse_paths_no_exist.add(bundle)

        if bundle.bundle_path.is_dir():
            invalid_dirs.add(bundle.bundle_path)
        elif bundle.bundle_path.is_file():
            bundle_paths_exist.add(bundle)
        else:
            bundle_paths_no_exist.add(bundle)

        browse_parent_dirs.add(bundle.browse_path.parent)

    for path in browse_parent_dirs:
        if path.is_file():
            invalid_files.add(path)

    if invalid_dirs:
        print(
            "FATAL: The following directories exist but should not:\n" +
            "    " + "\n    ".join(os.path.relpath(path)
                                   for path in invalid_dirs)
        )
        sys.exit(1)

    if invalid_files:
        print(
            "FATAL: The following files exist but should be empty directories " +
            "or not exist at all:\n" +
            "    " + "\n    ".join(os.path.relpath(path)
                                   for path in invalid_files)
        )
        sys.exit(1)

    if browse_but_no_bundle := browse_paths_exist & bundle_paths_no_exist:
        print(
            "WARNING: The following browse directories exist but have no corresponding " +
            "bundle files, they will be left alone:\n" +
            "    " + "\n    ".join(os.path.relpath(bundle.browse_path)
                                   for bundle in browse_but_no_bundle)
        )

    if bundle_but_no_browse := bundle_paths_exist & browse_paths_no_exist:
        print(
            "WARNING: The following bundle files exist but have no corresponding " +
            "browse directories, they will automatically be unpacked:\n" +
            "    " + "\n    ".join(os.path.relpath(bundle.bundle_path)
                                   for bundle in bundle_but_no_browse)
        )

    if browse_paths_are_empty:
        print(
            "WARNING: The following browse directories already exist, " +
            "but are empty:\n" +
            "    " + "\n    ".join(os.path.relpath(bundle.browse_path)
                                   for bundle in browse_paths_are_empty)
        )

    if not bundle_but_no_browse | bundle_paths_no_exist:
        print("INFO: There are no new bundles or browse directories to create.")
        sys.exit()

    bundles_not_cloned = set()
    repos_not_cloned = set()
    bundles_not_created = set()

    with tempfile.TemporaryDirectory() as work_dir:
        work_dir = Path(work_dir)

        for bundle in bundle_but_no_browse:
            print("INFO: Cloning bundle: {}".format(
                os.path.relpath(bundle.bundle_path)))

            clone_path = work_dir / bundle.name

            if not clone_repo(bundle.bundle_path, clone_path):
                bundles_not_cloned.add(bundle)

        bundles_not_to_copy = bundles_not_cloned | browse_but_no_bundle

        for bundle in bundle_paths_no_exist:
            print("INFO: Cloning repository: {}".format(bundle.repo.url))

            clone_path = work_dir / bundle.name
            bundle_path = work_dir / bundle.bundle_path.name

            if not clone_repo(bundle.repo.url, clone_path):
                repos_not_cloned.add(bundle)
                continue

            print("INFO: Creating bundle: {}".format(bundle_path))

            if not bundle_repo(clone_path, bundle_path):
                bundles_not_created.add(bundle)

        for bundle in browse_paths_are_empty:
            print("INFO: Removing empty browse directory: {}".format(
                os.path.relpath(bundle.browse_path)))
            bundle.browse_path.rmdir()

        for bundle in (bundle_but_no_browse | bundle_paths_no_exist) - bundles_not_to_copy:
            print("INFO: Moving repository files to browse directory: {}".format(
                os.path.relpath(bundle.browse_path)))
            assert not bundle.browse_path.is_dir()
            repo_path = work_dir / bundle.name
            shutil.rmtree(repo_path / ".git")
            shutil.move(repo_path, bundle.browse_path)

        for bundle in bundle_paths_no_exist - bundles_not_created:
            print("INFO: Moving bundle files to bundles directory: {}".format(
                os.path.relpath(bundle.bundle_path)))
            assert not bundle.bundle_path.is_file()
            bundle_path = work_dir / bundle.bundle_path.name
            shutil.move(bundle_path, bundle.bundle_path)

    if bundles_not_cloned:
        print(
            "WARNING: The following bundle files have not been cloned due to errors: \n" +
            "    " + "\n    ".join(os.path.relpath(bundle.bundle_path)
                                   for bundle in bundles_not_cloned)
        )

    if repos_not_cloned:
        print(
            "WARNING: The following repositories have not been cloned due to errors: \n" +
            "    " + "\n    ".join(os.path.relpath(bundle.repo.url)
                                   for bundle in repos_not_cloned)
        )

    if bundles_not_created:
        print(
            "WARNING: The following bundle files have not been created due to errors: \n" +
            "    " + "\n    ".join(os.path.relpath(bundle.bundle_path)
                                   for bundle in bundles_not_created)
        )


if __name__ == "__main__":
    REPO_LIST_FILE = "./repo_list.txt"
    REPO_BROWSE_DIR = "./browse/"
    REPO_BUNDLE_DIR = "./bundle/"

    main(REPO_LIST_FILE, REPO_BROWSE_DIR, REPO_BUNDLE_DIR)
