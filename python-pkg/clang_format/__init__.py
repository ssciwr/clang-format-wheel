'''init'''
import os
import sys

import pkg_resources


def _run(name):
    '''wrappers for executables

    newer setuptools don't allow binary files as entrypoints/scripts in
    setup.py, so this is a way to have an entry point for each binary
    '''
    bin_path = pkg_resources.resource_filename('clang_format', 'bin')
    os.execv(os.path.join(bin_path, name), [name, ] + sys.argv[1:])


def clang_format():
    '''wrapper for clang-format'''
    _run('clang-format')
