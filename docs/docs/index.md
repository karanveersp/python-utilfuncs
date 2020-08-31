# Welcome to utilfuncs

## Installation

The library can be installed from source. 
```
git clone https://github.com/karanveersp/python-utilfuncs
cd python-utilfuncs
pip install --editable .
```
If you want to update the installation later, just run `git pull` in the python-utilfuncs directory and the
updates will take effect.

## Usage

```python
import utilfuncs as util

for i, row in enumerate(util.get_rows("my_file.csv", delimiter="\t")):
    print(f"Row {i}: {row}")
```

After importing the module as util, all the functions are directly accessible.