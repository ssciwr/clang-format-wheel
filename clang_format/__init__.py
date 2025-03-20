import os
import subprocess
import sys


def get_executable(name):
    return os.path.join(os.path.dirname(__file__), "data", "bin", name)

def _run(name):
    executable = get_executable(name)
    return subprocess.call([executable] + sys.argv[1:])

def clang_format():
    raise SystemExit(_run("clang-format"))
