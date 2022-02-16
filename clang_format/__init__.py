import os
import subprocess
import sys


def _run(name):
    executable = os.path.join(os.path.dirname(__file__), "data", "bin", name)
    return subprocess.call([executable] + sys.argv[1:])


def clang_format():
    raise SystemExit(_run("clang-format"))


def clang_format_diff():
    raise SystemExit(_run("clang-format-diff.py"))


def git_clang_format():
    raise SystemExit(_run("git-clang-format"))
