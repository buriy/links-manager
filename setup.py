#!/usr/bin/env python

import os
from setuptools import setup, find_packages
import links_manager

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def desc():
    info = read('README')
    try:
        return info + '\n\n' + read('docs/changelog.rst')
    except IOError:
        # no docs
        return info

setup(
    name = 'links_manager',
    description = 'Python command-line utility to make symbolic links (symlinks) '
                  'management much easier across various platforms.',
    long_description = desc(),
    license = 'BSD',
    version = "0.1",
    author = "Yuri Baburov",
    author_email = "burchik@gmail.com",
    url = 'https://github.com/buriy/links-manager',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
        ],
    py_modules = ['manage-links', 'links_manager'],
    packages = find_packages(exclude=[]),
    platforms='any',
    entry_points = """
    [console_scripts]
    manage-links=links_manager.manage_links:main
    """
)
