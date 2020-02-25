from setuptools import setup, find_packages

setup(
    name='utilfuncs',
    version='20.2.25',
    author="Karanveer Plaha",
    author_email="karan_4496@hotmail.com",
    url="https://github.com/karanveersp/python-utilfuncs",
    description="Simple utility functions for general use.",
    packages=find_packages(exclude="tests"),
    tests_require=["pytest"],
    install_requires=[
        'pdoc3',
        'pipreqs',
    ]
)
