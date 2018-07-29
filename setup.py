#!/usr/bin/env python
import os
from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='mite',
    author='Veit Heller',
    version='0.0.2',
    license='MIT',
    url='https://github.com/port-zero/mite',
    description='A modern Mite wrapper for Python',
    long_description=long_description,
    download_url = 'https://github.com/port-zero/mite/tarball/0.0.2',
    packages=find_packages('.'),
    install_requires=[
        "requests",
    ]
)

