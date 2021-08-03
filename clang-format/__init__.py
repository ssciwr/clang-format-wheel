import os
import sys


def clang_format():
    name = "clang-format"
    executable = os.path.join(os.path.split(__file__)[0], "bin", name)
    return os.execv(executable, [name] + sys.argv[1:])
