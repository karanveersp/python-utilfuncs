"""
Utility csv functions for reading/writing/appending data.
"""
import csv as pycsv
from typing import Any, Generator, List
from utilfuncs.common import *

def get_rows(csvpath: PathLike, skip_header=False, delimiter=",", encoding="utf-8") -> Generator[List[str], None, None]:
    """
    get_rows yields rows from the csv file specified.
    The caller must iterate over the returned generator
    to receive the rows.

    Args:
        csvpath: Path to csv file
        skip_header: Whether to skip header row, default False
        delimiter: Row delimiter character, default ","
        encoding: File encoding, default "utf-8"

    Yields:
        List of strings representing rows
    """
    with open(csvpath, "r", encoding=encoding) as csvfile:
        reader = pycsv.reader(csvfile, delimiter=delimiter)
        for row in reader:
            if skip_header:
                skip_header = False
                continue
            yield row


def write_rows(csvpath: PathLike, list_of_rows: List[List[str]], delimiter=",", encoding="utf-8") -> None:
    """
    Write rows to csv file.

    Args:
        csvpath: Path to csv file
        list_of_rows: 2D list of strings
        delimiter: Row delimiter character, default ","
        encoding: File encoding, default "utf-8"
    """
    with open(csvpath, "w", newline="", encoding=encoding) as csvfile:
        writer = pycsv.writer(csvfile, delimiter=delimiter)
        writer.writerows(list_of_rows)


def append_row(csvpath: PathLike, row: List[str], delimiter=",", encoding="utf-8") -> None:
    """
    Appends a single row to the csv file specified.
    The file must already exist.

    Args:
        csvpath: path to csv file
        row: A list of strings
        delimiter: Row delimiter, defaults to ","
        encoding: File encoding, defaults to "utf-8"
    """
    with open(csvpath, "a", newline="", encoding=encoding) as csvfile:
        writer = pycsv.writer(csvfile, delimiter=delimiter)
        writer.writerow(row)


def append_rows(csvpath: PathLike, list_of_rows: List[List[str]], delimiter=",", encoding="utf-8"):
    """
    Appends multiple rows to the csv file specified.
    The file must already exist.

    Args:
        csvpath: path to csv file
        list_of_rows: 2D list of strings
        delimiter: Row delimiter, defaults to ","
        encoding: File encoding, defaults to "utf-8"
    """
    with open(csvpath, "a", newline="", encoding=encoding) as csvfile:
        writer = pycsv.writer(csvfile, delimiter=delimiter)
        for row in list_of_rows:
            writer.writerow(row)


def get_rows_by_column_filter(filepath: PathLike, col_index: int, col_value: Any, delimiter=",", encoding="utf-8") -> Generator[List[str], None, None]:
    """
    Returns rows where certain values occur in a certain column. Like v-lookups in excel.

    Args:
        filepath: Path of file
        col_index: 0 based col index on which to filter on
        col_value: Value of column to filter on
        delimiter: Row delimiter. Defaults to ",".
        encoding: File encoding. Defaults to "utf-8".

    Yields:
        List of strings representing rows
    """
    for row in get_rows(filepath, delimiter=delimiter, encoding=encoding):
        if row[col_index] == col_value:
            yield row
