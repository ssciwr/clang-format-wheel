import importlib
from setuptools import setup

VERSION = (importlib
           .machinery
           .SourceFileLoader('version', 'clang_format/version.py')
           .load_module()
           .__version__
           )

with open('README.md', 'r') as fd:
    long_description = fd.read()

setup(
    name='clang-format',
    version=VERSION,
    author='mgevaert',
    author_email='clang-format@gevaert.ca',
    packages=['clang_format'],
    url='http://clang.llvm.org/',
    download_url='http://releases.llvm.org/download.html',
    project_urls={
        "Documentation": 'https://clang.llvm.org/docs/ClangFormat.html',
        "Source Code": 'https://github.com/mgevaert/clang-format-wheel',
    },
    description='pip installable clang-format',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: C',
        'Programming Language :: C++',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools'
        ],
    license='Apache 2.0',
    keywords='clang-format',
    install_requires=[],
    tests_require=[],
    setup_requires=[],
    scripts=['clang_format/bin/clang-format-diff.py',
             'clang_format/bin/git-clang-format',
             ],
    entry_points={
        'console_scripts': [
            'clang-format=clang_format:clang_format',
        ]
    },
    include_package_data=True,
    )
