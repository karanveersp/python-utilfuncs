from setuptools import setup, find_packages
from utilfuncs import __version__

import codecs
import os
import re

here = os.path.abspath(os.path.dirname(__file__))

def find_version(*parts):
    """
    Figure out version number without importing the package.
    https://packaging.python.org/guides/single-sourcing-package-version/
    """
    with codecs.open(os.path.join(here, *parts), 'r', errors='ignore') as fp:
        version_file = fp.read()
    version_match = re.search(r"^__version__ = ['\"](.*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


version = find_version('utilfuncs', '__init__.py')

setup(
    name='utilfuncs',
    version=version,
    description="Simple utility functions for general use.",
    author="Karanveer Plaha",
    author_email="karan_4496@hotmail.com",
    url="https://github.com/karanveersp/python-utilfuncs",
    packages=find_packages('.', exclude=['tests']),
    install_requires=open('requirements.txt', 'r').read().splitlines(),
    tests_require=open('test_requirements.txt', 'r').read().splitlines(),
    setup_requires=[
        'pytest-runner'
    ],
    extras_require={
        "dev": [ # install the dev extras using `pip install -e .[dev] after cloning`
            "pytest",
            "sphinx",
            "sphinx_rtd_theme"
        ]
    },
    # install_requires=[
    #     'pdoc3',
    #     'pipreqs',
    # ]
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Topic :: Utilities"
    ]
)
