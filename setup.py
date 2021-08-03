from skbuild import setup


setup(
    name="clang-format",
    version="0.0.3",
    author="Dominic Kempf",
    author_email="ssc@iwr.uni-heidelberg.de",
    packages=["clang-format"],
    zip_safe=False,
    entrypoints={
        "clang-format": [
            "clang-format=clang-format:clang-format"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)
