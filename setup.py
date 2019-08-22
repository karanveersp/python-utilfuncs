from setuptools import setup, find_packages

setup(
    name='utilfuncs',
    version='0.1.0',
    description='Utility functions for file/csv',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'pdoc3',
        'pipreqs',
        'pytest',
        'pytest-mock',
    ]
)
