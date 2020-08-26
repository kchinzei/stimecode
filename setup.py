#!-*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages
import timecode

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGELOG.rst')).read()

setup(
    name='timecode',
    version=timecode.__version__,
    description="SMPTE Time Code Manipulation Library",
    long_description='%s\n\n%s' % (README, CHANGES),
    long_description_content_type='text/x-rst',
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    author=['Erkan Ozgur Yilmaz'],
    author_email=['eoyilmaz@gmail.com'],
    url='https://github.com/eoyilmaz/timecode',
    keywords=['video', 'timecode', 'smpte'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
)
