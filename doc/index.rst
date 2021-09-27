.. mdinclude:: ../README.md

How to add a release
--------------------

These are the steps necessary to add a new release to PyPI:

* Change the version identifier in :code:`clang-format_version.cmake` to a version which has been releases on the LLVM GitHub page.
* Commit the change to the repository
* Create a release on GitHub

The release creation automatically triggers a GitHub actions pipeline that build wheels for a variety of platforms and publishes them on PyPI.
