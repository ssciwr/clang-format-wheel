from skbuild import setup
import versioneer

setup(
    name="clang-format",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author="Dominic Kempf",
    author_email="ssc@iwr.uni-heidelberg.de",
    packages=["clang-format"],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
)
