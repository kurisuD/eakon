# coding=utf-8
import setuptools

with open("README.md") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eakon",
    version="0.0.5",
    author="KurisuD",
    author_email="KurisuD@pypi.darnand.net",
    description="A simple library to control (japanese) air-conditioners",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KurisuD/eakon",
    packages=setuptools.find_packages(),
    install_requires=['bitstring', 'pathlib'],
    classifiers=[
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "License :: Public Domain",
        "Operating System :: POSIX :: Linux",
        "Topic :: Home Automation"
    ],
)
