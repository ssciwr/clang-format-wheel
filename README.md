# Goal

Precompiled python wheels containing the clang-format and python support files.
Thus, one has pip installable clang-format useful for CI/CD, and local formatting
changes, with a stable output, as long as the same version is used.

# Versions

The idea is to track all officially released clang-format versions


# General Outline

1. LLVM and clang source is downloaded by host_actions.sh
2. Docker image from quay.io/pypa/manylinux1_x86_64 is loaded
3. In the container:
3.1 CMake is built (currently the cmake wheels don't work on manylinux1)
3.2 Each of the desired clang-format binaries are statically built
3.3 A python package skeleton is copied, and used by `bdist_wheel`
3.4 `auditwheel repair` is used to make sure no library dependencies exist,
    and that the package is self-contained
4. Packages are uploaded via twine

# Adding a new version

1.
