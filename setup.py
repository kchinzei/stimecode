#!-*- coding: utf-8 -*-

import re
import os
from setuptools import setup, find_packages


def read_file(file_path):
    """Read the given file at file_path.

    Args:
        file_path (str): The file path to read.

    Returns:
        str: The file content.
    """
    with open(file_path) as f:
        data = f.read()
    return data


here = os.path.abspath(os.path.dirname(__file__))
README = read_file(os.path.join(here, 'README.rst'))
CHANGES = read_file(os.path.join(here, 'CHANGELOG.rst'))
METADATA = read_file(os.path.join(here, "timecode", "__init__.py"))


def get_meta(meta):
    """Return meta.

    Args:
        meta (str): The meta to read. i.e. ``version``, ``author`` etc.
    """
    meta_match = re.search(
        r"^__{meta}__ = ['\"]([^'\"]*)['\"]".format(meta=meta),
        METADATA, re.M
    )
    if meta_match:
        meta_value = meta_match.group(1)
        return meta_value


setup(
    name=get_meta("name"),
    version=get_meta("version"),
    description=get_meta("description"),
    long_description='%s\n\n%s' % (README, CHANGES),
    long_description_content_type='text/x-rst',
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    author=get_meta("author"),
    author_email=get_meta("author_email"),
    url=get_meta("url"),
    keywords=['video', 'timecode', 'smpte'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
)
