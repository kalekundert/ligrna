#!/usr/bin/env python3
# encoding: utf-8

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import re
with open('sgrna_sensor/__init__.py') as file:
    version_pattern = re.compile("__version__ = '(.*)'")
    version = version_pattern.search(file.read()).group(1)

with open('README.rst') as file:
    readme = file.read()

setup(
    name='sgrna_sensor',
    version=version,
    author='Kale Kundert',
    author_email='kale.kundert@ucsf.edu',
    description='',
    long_description=readme,
    url='https://github.com/kalekundert/sgrna_sensor',
    keywords=[
        'sgrna_sensor',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
    license='MIT',
    packages=[
        'sgrna_sensor',
    ],
    install_requires=[
        'docopt',
        'matplotlib',
        'numpy',
        'regex',
    ],
    entry_points={
        'console_scripts': [
            'sgrna_sensor = sgrna_sensor.show_seqs:main',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
