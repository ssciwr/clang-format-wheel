# clang-format Python distribution

[![PyPI Release](https://img.shields.io/pypi/v/clang-format.svg)](https://pypi.org/project/clang-format)

This project packages the `clang-format` utility as a Python package. It allows you to install `clang-format` directly from PyPI:

```
python -m pip install clang-format
```

This projects intends to release a new PyPI package for each major and minor release of `clang-format`.

## Building new releases

The [clang-format-wheel repository](https://github.com/ssciwr/clang-format-wheel) provides the build logic to build and publish binary wheels of the `clang-format` utility.

In order to add a new release, the following steps are necessary:

* Edit the [version file](https://github.com/ssciwr/clang-format-wheel/blob/main/clang-format_version.cmake) to reflect the new version.
* Make a GitHub release to trigger the [GitHub Actions release workflow](https://github.com/ssciwr/clang-format-wheel/actions/workflows/release.yml). Alternatively, the workflow can be triggered manually.

On manual triggers, the following input variables are available:
* `use_qemu`: Whether to build targets that require emulation (default: `true`)
* `llvm_version`: Override the LLVM version (default: `""`)
* `wheel_version`: Override the wheel packaging version (default `"0"`)

## Acknowledgments

This repository extends the great work of several other projects:

* `clang-format` itself is [provided by the LLVM project](https://github.com/llvm/llvm-project) under the Apache 2.0 license with exceptions.
* The build logic is based on [scikit-build](https://github.com/scikit-build/scikit-build) which greatly reduces the amount of low level code necessary to package `clang-format`.
* The `scikit-build` packaging examples of [CMake](https://github.com/scikit-build/cmake-python-distributions) and [Ninja](https://github.com/scikit-build/ninja-python-distributions) were very helpful in packaging `clang-format`.
* The CI build process is controlled by [cibuildwheel](https://github.com/pypa/cibuildwheel) which makes building wheels across a number of platforms a pleasant experience (!)

Special thanks goes to mgevaert who initiated this project and maintained it until 2021.

We are grateful for the generous provisioning with CI resources that GitHub currently offers to Open Source projects.
