#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Licensed under the terms of the BSD 3-Clause License
# (see LICENSE for details)
# https://github.com/mysmarthub
# Copyright © 2020-2021 Aleksandr Suvorov
# -----------------------------------------------------------------------------
from setuptools import setup, find_packages
from os.path import join, dirname

PACKAGE = "smartcleaner"
VERSION = __import__(PACKAGE).__version__
AUTHOR = __import__(PACKAGE).__author__
AUTHOR_EMAIL = "myhackband@yandex.ru"
DESCRIPTION = "Graphical utility for destroying, zeroing, and deleting files, " \
              "to complicate or completely impossible to restore them." \
              " Aleksandr Suvorov | https://github.com/mysmarthub/smartcleaner | " \
              "Donate: 4276 4417 5763 7686 | 4048 " \
              "4150 0400 5852 "
NAME = "smartcleaner"
URL = "https://github.com/mysmarthub/smartcleaner"
LICENSE = 'BSD 3-Clause'
LONG_DESCRIPTION = open(join(dirname(__file__), 'README.md')).read()
# INSTALL_REQUIRES = open(join(dirname(__file__), 'requirements.txt')).read()
INSTALL_REQUIRES = ['pyside2', ]
PLATFORM = ['Linux, Windows']
CLASSIFIERS = [
    "License :: OSI Approved :: BSD License",
    "Operating System :: OS Independent",
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Intended Audience :: End Users/Desktop",
    "Intended Audience :: System Administrators",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python :: 3 :: Only",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities"
]
KEYWORDS = [
    'smart cleaner',
    'shred files',
    'zero files',
    'del files',
    'cleaner',
    'smartcleaner',
    'shred',
    'my cleaner',
    'aleksandr suvorov',
    'smart-py.ru',
    'hack band',
    'smart files destroyer'
]
setup(
    name=NAME,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    description=DESCRIPTION,
    version=VERSION,
    license=LICENSE,
    platforms=PLATFORM,
    packages=find_packages(),
    long_description_content_type='text/markdown',
    long_description=LONG_DESCRIPTION,
    install_requires=INSTALL_REQUIRES,
    include_package_data=True,
    zip_safe=False,
    keywords=KEYWORDS,
    entry_points={
        'gui_scripts':
            ['smartcleaner = smartcleaner.smart_cleaner:main']
    }
)
