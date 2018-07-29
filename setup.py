#!/usr/bin/env python
import os
from setuptools import setup, find_packages

setup(
    name='mite',
    author='Veit Heller',
    version='0.0.1',
    license='MIT',
    url='https://github.com/port-zero/mite',
    description='A modern Mite wrapper for Python',
    download_url = 'https://github.com/port-zero/mite/tarball/0.0.1',
    packages=find_packages('.'),
    install_requires=[
        "requests",
    ]
)

