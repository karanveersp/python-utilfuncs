# Python Utility Library

[![Documentation Status](https://readthedocs.org/projects/python-utilfuncs/badge/?version=latest)](https://python-utilfuncs.readthedocs.io/en/latest/?badge=latest)


## Installation
```bash
git clone https://github.com/karanveersp/python-utilfuncs
cd python-utilfuncs
pip install --editable .
```

To install the package with test dependencies for unit testing
```bash
pip install --editable .[dev]
```


## Run tests
```bash
cd python-utilfuncs
pytest
```

Import the library:
    `import utilfuncs as util`
    
Use the library:
    `util.get_rows(csvpath, skip_header=True)`

After importing the utilfuncs module as util, all the functions are directly accessible.

## To build the documentation

```
pip install sphinx
cd docs
./make html
```
The HTML pages are in _build\html


## Contrubutors
- Karanveer Plaha
- Manisha Mahender