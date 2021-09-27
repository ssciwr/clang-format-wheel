
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
from skbuild import setup

import re

class genericpy_bdist_wheel(_bdist_wheel):
    def finalize_options(self):
        _bdist_wheel.finalize_options(self)
        self.root_is_pure = False

    def get_tag(self):
        python, abi, plat = _bdist_wheel.get_tag(self)
        python, abi = "py2.py3", "none"
        return python, abi, plat

# Read the clang-format version from the "single source of truth"
def get_version():
    with open("clang-format_version.cmake", "r") as version_file:
        parsed = {}
        for line in version_file:
            match = re.match("set\((.*) (.*)\)", line)
            if len(match.groups()) != 2:
                raise ValueError("Version File not readable")
            parsed[match.groups()[0]] = match.groups()[1]
        if parsed['CLANG_FORMAT_WHEEL_VERSION'] == "0":
            return f"{parsed['CLANG_FORMAT_VERSION']}"
        else:
            return f"{parsed['CLANG_FORMAT_VERSION']}.{parsed['CLANG_FORMAT_WHEEL_VERSION']}"


# Parse the given README file
with open("README.md", "r") as readme_file:
    readme = readme_file.read()

cmdclass = {"bdist_wheel": genericpy_bdist_wheel}
setup(
    name="clang-format",
    version=get_version(),
    cmdclass=cmdclass,
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
    description="Clang-Format is an LLVM-based code formatting tool",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="http://clang.llvm.org/",
    project_urls={
        "Documentation": "https://clang.llvm.org/docs/ClangFormat.html",
        "Source": "https://github.com/ssciwr/clang-format-wheel"
    },
    download_url="https://github.com/llvm/llvm-project/releases",
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
