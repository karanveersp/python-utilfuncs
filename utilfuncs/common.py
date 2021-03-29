from typing import Union
import pathlib

class Error(Exception):
    """Base class for all exceptions raised by this package"""

class InvalidDirectoryPath(Error):
    """The path specified was not a valid directory"""


PathLike = Union[pathlib.Path, str]
