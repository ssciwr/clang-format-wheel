import os
import subprocess
import sys


def _get_executable(name):
    return os.path.join(os.path.dirname(__file__), "data", "bin", name)


def _run(name):
    executable = _get_executable(name)
    return subprocess.call([executable] + sys.argv[1:])


def clang_format():
    result = _run("clang-format")
    pmi_post_format(sys.argv[1:])
    raise SystemExit(result)


def pmi_post_format(files):
    for f in files:
        if ".cpp" in f or ".h" in f:
            fix_pmi_macros_formatting(f)
        elif "--version" in f:
            print("pmi-clang-format")


def fix_pmi_macros_formatting(file_path):
    patterns = ["ree;", "rrr;", "nee;", "co_ree;"]
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

        updated_lines = []
        for i in range(len(lines)):
            if (
                i > 0
                and (lines[i].strip() in patterns)
                and lines[i - 1].endswith(";\n")
            ):
                # Combine the previous line with the current line
                updated_lines[-1] = (
                    updated_lines[-1].rstrip() + " " + lines[i].strip() + "\n"
                )
            else:
                updated_lines.append(lines[i])

        with open(file_path, "w") as file:
            file.writelines(updated_lines)
    except Exception as e:
        print(f"An error occurred when formatting {file_path}: {e}")
