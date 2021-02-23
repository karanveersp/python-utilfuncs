"""
Utility csv functions for reading/writing/appending data.
"""
import csv as pycsv


def get_rows(csvpath, skip_header=False, delimiter=",", encoding="utf-8"):
    """
    get_rows yields rows from the csv file specified.
    The caller must iterate over the returned generator
    to receive the rows.

    :param csvpath: Path to csv file

    :param skip_header: Whether to skip header row, default False
    :type skip_header: bool

    :param delimiter: Row delimiter character, default ","
    :type delimiter: str

    :param encoding: File encoding, default "utf-8"
    :type encoding: str

    :return: generator that can be iterated to receive rows
    :rtype: generator
    """
    with open(csvpath, "r", encoding=encoding) as csvfile:
        reader = pycsv.reader(csvfile, delimiter=delimiter)
        for row in reader:
            if skip_header:
                skip_header = False
                continue
            yield row


def write_rows(csvpath, list_of_rows, delimiter=",", encoding="utf-8"):
    """
    Write rows to csv file.

    :param csvpath: path to csv file
    :type csvpath: path like
    :param list_of_rows: 2D list of rows
    :type list_of_rows: list(list(str))
    :param delimiter: Row delimiter, defaults to ","
    :type delimiter: str, optional
    :param encoding: File encoding, defaults to "utf-8"
    :type encoding: str, optional
    """
    with open(csvpath, "w", newline="", encoding=encoding) as csvfile:
        writer = pycsv.writer(csvfile, delimiter=delimiter)
        writer.writerows(list_of_rows)


def append_row(csvpath, row, delimiter=",", encoding="utf-8"):
    """
    Appends a single row to the csv file specified.
    The file must already exist.

    :param csvpath: path to csv file
    :type csvpath: path like
    :param row: A list of strings
    :type row: list(str)
    :param delimiter: Row delimiter, defaults to ","
    :type delimiter: str, optional
    :param encoding: File encoding, defaults to "utf-8"
    :type encoding: str, optional
    """
    with open(csvpath, "a", newline="", encoding=encoding) as csvfile:
        writer = pycsv.writer(csvfile, delimiter=delimiter)
        writer.writerow(row)


def append_rows(csvpath, list_of_rows, delimiter=",", encoding="utf-8"):
    """
    Appends multiple rows to the csv file specified.
    The file must already exist.

    :param csvpath: path to csv file
    :type csvpath: path like
    :param list_of_rows: 2D list of rows
    :type list_of_rows: list(list(str))
    :param delimiter: Row delimiter, defaults to ","
    :type delimiter: str, optional
    :param encoding: File encoding, defaults to "utf-8"
    :type encoding: str, optional'
    """
    with open(csvpath, "a", newline="", encoding=encoding) as csvfile:
        writer = pycsv.writer(csvfile, delimiter=delimiter)
        for row in list_of_rows:
            writer.writerow(row)


def get_rows_by_column_filter(filepath, col_index, col_value, delimiter=",", encoding="utf-8"):
    for row in get_rows(filepath, delimiter=delimiter, encoding=encoding):
        if row[col_index] == col_value:
            yield row
