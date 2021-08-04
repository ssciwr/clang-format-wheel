import os
import sys


def _run(name):
    executable = os.path.join(os.path.split(__file__)[0], "data", "bin", name)
    return os.execv(executable, [name] + sys.argv[1:])


def clang_format():
    return _run("clang-format")


def clang_format_diff():
    return _run("clang-format-diff.py")


def git_clang_format():
    return _run("git-clang-format")
