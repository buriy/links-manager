#!/usr/bin/env python

import os
from setuptools import setup
import releaser

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
    name = 'releaser',
    description = 'command line parsing speedster',
    long_description = desc(),
    license = 'BSD',
    version = releaser.__version__,
    author = releaser.__author__,
    author_email = releaser.__email__,
    url = 'http://hg.piranha.org.ua/releaser/',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
        ],
    py_modules = ['release', 'releaser'],
    platforms='any',
    )
