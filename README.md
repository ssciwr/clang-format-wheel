# clang-format Python distribution

[![PyPI Release](https://img.shields.io/pypi/v/clang-format.svg)](https://pypi.org/project/clang-format)

This project packages the `clang-format` utility as a Python package. It allows you to install `clang-format` directly from PyPI:

```
python -m pip install clang-format
```

This projects intends to release a new PyPI package for each major and minor release of `clang-format`.

## Use with pipx

You can use `pipx` to run clang-format, as well. For example, `pipx run clang-format <args>` will run clang-format without any previous install required on any machine with pipx (including all default GitHub Actions / Azure runners, avoiding requiring a pre-install step or even `actions/setup-python`).

## Use from pre-commit

A [pre-commit](https://pre-commit.com) hook is also [provided](https://github.com/pre-commit/mirrors-clang-format), use like this:

```yaml
- repo: https://github.com/pre-commit/mirrors-clang-format
  rev: v21.1.0
  hooks:
  - id: clang-format
    types_or: [c++, c, cuda]
```

In contrast to many other pre-commit hooks, the versioning of the hook matches the versioning of `clang-format`.

If you are required to stick with a given major/minor version of `clang-format` with your pre-commit-hook, you can use [this alternative hook repository](https://github.com/ssciwr/clang-format-hook) that also receives backports of older versions of clang-format.
Currently, all major/minor versions of LLVM >= 10 are supported.
It is best to subscribe to releases of the hook repository to get notified of new backport releases, as `pre-commit`'s auto-upgrade functionality will not work in that case.

## Building new releases

The [clang-format-wheel repository](https://github.com/ssciwr/clang-format-wheel) provides the logic to build and publish binary wheels of the `clang-format` utility.

In order to add a new release, the following steps are necessary:

* Edit the [version file](https://github.com/ssciwr/clang-format-wheel/blob/main/clang-format_version.txt)
  * In the form `llvm_version.wheel_version`, e.g. `18.0.2.1`
* Tag the commit with this version to trigger the [GitHub Actions release workflow](https://github.com/ssciwr/clang-format-wheel/actions/workflows/release.yml)
  * e.g. `git tag v18.0.2.1 && git push origin v18.0.2.1`

Alternatively, the workflow can be triggered manually:

On manual triggers, the following input variables are available:
* `llvm_version`: Override the LLVM version (default: `""`)
* `wheel_version`: Override the wheel packaging version (default `"0"`)
* `skip_emulation`: Set which emulation builds to skip, e.g. `"qemu"` (default: `""`)
* `deploy_to_testpypi`: Whether to deploy to TestPyPI instead of PyPI (default: `false`)

The repository with the precommit hook is automatically updated using a scheduled Github Actions workflow.

## Acknowledgements

This repository extends the great work of several other projects:

* `clang-format` itself is [provided by the LLVM project](https://github.com/llvm/llvm-project) under the Apache 2.0 License with LLVM exceptions.
* The build logic is based on [scikit-build-core](https://github.com/scikit-build/scikit-build-core) which greatly reduces the amount of low level code necessary to package `clang-format`.
* The `scikit-build` packaging examples of [CMake](https://github.com/scikit-build/cmake-python-distributions) and [Ninja](https://github.com/scikit-build/ninja-python-distributions) were very helpful in packaging `clang-format`.
* The CI build process is controlled by [cibuildwheel](https://github.com/pypa/cibuildwheel) which makes building wheels across a number of platforms a pleasant experience (!)

Special thanks goes to mgevaert who initiated this project and maintained it until 2021.

We are grateful for the generous provisioning with CI resources that GitHub currently offers to Open Source projects.
