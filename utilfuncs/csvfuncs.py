import csv
import os
from pathlib import Path

def get_rows(csvpath):
    """
    get_rows yields rows from the csv file specified.
    The caller must iterate over the returned generator
    to receive the rows.
    If the csv path is not a valid file, an exception
    will be raised when attempting iteration.

    Args:
        csvpath: Path to csv file
    
    Returns:
        Generator that can be iterated on to
        receive rows.
    """
    with open(csvpath, "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            yield row


def write_rows(csvpath, list_of_rows):
    """
    write_rows writes rows to the csv file specified.
    If the file already exists, it will be overwritten.

    Args:
        csvpath: Path to csv file
        list_of_rows: A 2D list where each item is a row.
    """
    with open(csvpath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(list_of_rows)


def append_row(csvpath, row):
    """
    Appends a single row to the csv file specified.
    The file must already exist.

    Args:
        csvpath: Path to csv file
        row: List of values representing a row
    """
    with open(csvpath, "a", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(row)


def append_rows(csvpath, list_of_rows):
    """
    Appends multiple rows to the csv file specified.
    The file must already exist.

    Args:
        csvpath: Path to csv file
        list_of_rows: A 2D list where each item is a row
    """
    for row in list_of_rows:
        append_row(csvpath, row)
