from setuptools import setup, find_packages

setup(
    name='utilfuncs',
    version='20.2.25',
    description='Utility functions for general use',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'pdoc3',
        'pipreqs',
        'pytest',
        'pytest-mock',
    ]
)
