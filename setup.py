from setuptools import setup, find_packages

setup(
    name='utilfuncs',
    version='20.2.25',
    description="Simple utility functions for general use.",
    author="Karanveer Plaha",
    author_email="karan_4496@hotmail.com",
    url="https://github.com/karanveersp/python-utilfuncs",
    package_dir={'': 'src'},
    packages=["utilfuncs"],
    install_requires=[
        "mkdocs",
        "mkdocs-material",
        "mkdocstrings"
    ],
    extras_require={
        "dev": [ # install the dev extras using `pip install -e .[dev] after cloning`
            "pytest>=3.7"
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
