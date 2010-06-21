#!/usr/bin/env python

import os
from setuptools import setup
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
    version = links_manager.__version__,
    author = links_manager.__author__,
    author_email = links_manager.__email__,
    url = '',
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
    platforms='any',
    )
