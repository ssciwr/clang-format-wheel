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
    patterns = [
        "ree;",
        "co_ree;",
        "eee_absorb;",
        "nee;",
        "rrr;",
        "co_ree;",
        "ree_silent;",
        "co_ree_silent;",
        "e_result(",
        "co_e_result(",
        "e_result_silent(",
        "co_e_result_silent(",
        "e_return(",
        "co_e_return(",
        "e_return_silent(",
        "co_e_return_silent(",
        "e_obj_exec(",
        "e_result_return(",
        "co_e_result_return(",
        "nee_result(",
        "e_err(",
        "co_e_err(",
        "e_exec(",
        "e_result_return_silent(",
        "co_e_result_return_silent(",
    ]

    try:
        with open(file_path, "r") as file:
            lines = file.readlines()

        updated_lines = []
        for i, line in enumerate(lines):
            if (
                i > 0
                and any(line.strip().startswith(pattern) for pattern in patterns)
                and lines[i - 1].endswith(";\n")
            ):
                # Combine the previous line with the current line
                updated_lines[-1] = (
                    updated_lines[-1].rstrip() + " " + line.strip() + "\n"
                )
            else:
                updated_lines.append(line)

        with open(file_path, "w") as file:
            file.writelines(updated_lines)
    except Exception as e:
        print(f"An error occurred when formatting {file_path}: {e}")
