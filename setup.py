from skbuild import setup

import re


# Read the clang-format version from the "single source of truth"
def get_version():
    with open("clang-format_version.cmake", "r") as version_file:
        version_line = version_file.read()
        match = re.match("set\(CLANG_FORMAT_VERSION (.*)\)", version_line)
        if not match:
            raise ValueError("Version File not readable")
        return match.groups()[0]


setup(
    name="clang-format",
    version="0.0.7",
    author="Dominic Kempf",
    author_email="ssc@iwr.uni-heidelberg.de",
    packages=["clang_format"],
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "clang-format=clang_format:clang_format",
            "git-clang-format=clang_format:git_clang_format",
            "clang-format-diff.py=clang_format:clang_format_diff"
        ]
    },
    classifiers=[
        "Programming Language :: C",
        "Programming Language :: C++",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
    ],
    license="Apache 2.0"
)
