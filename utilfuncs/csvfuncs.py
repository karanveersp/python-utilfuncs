import csv


def get_rows(csvpath, skip_header=False, delimiter=",", encoding="utf-8"):
    """
    get_rows yields rows from the csv file specified.
    The caller must iterate over the returned generator
    to receive the rows.

    Args:
        csvpath: Path to csv file
        skip_header (bool): Whether to skip header row
        delimiter (str): Default ","
        encoding (str): Default 'utf-8'

    Returns:
        Generator that can be iterated on to
        receive rows.
    """
    with open(csvpath, "r", encoding=encoding) as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        for row in reader:
            if skip_header:
                skip_header = False
                continue
            yield row


def write_rows(csvpath, list_of_rows, delimiter=",", encoding="utf-8"):
    """
    write_rows writes rows to the csv file specified.
    If the file already exists, it will be overwritten.
    If the file doesn't exist, it will be created and the
    rows will be written to it.

    Args:
        csvpath: Path to csv file
        list_of_rows: A 2D list where each item is a row
        delimiter (str): Default ","
        encoding (str): Default 'utf-8'
    """
    with open(csvpath, "w", newline="", encoding=encoding) as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter)
        writer.writerows(list_of_rows)


def append_row(csvpath, row, delimiter=",", encoding="utf-8"):
    """
    Appends a single row to the csv file specified.
    The file must already exist.

    Args:
        csvpath: Path to csv file
        row: List of values representing a row
        delimiter (str): Default ","
        encoding (str): Default 'utf-8'
    """
    with open(csvpath, "a", newline="", encoding=encoding) as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter)
        writer.writerow(row)


def append_rows(csvpath, list_of_rows, delimiter=",", encoding="utf-8"):
    """
    Appends multiple rows to the csv file specified.
    The file must already exist.

    Args:
        csvpath: Path to csv file
        list_of_rows: A 2D list where each item is a row
        delimiter (str): Default ","
        encoding (str): Default 'utf-8'
    """
    with open(csvpath, "a", newline="", encoding=encoding) as csvfile:
        writer = csv.writer(csvfile, delimiter=delimiter)
        for row in list_of_rows:
            writer.writerow(row)


def get_rows_by_column_filter(filepath, col_index, col_value, delimiter=",", encoding="utf-8"):
    for row in get_rows(filepath, delimiter=delimiter, encoding=encoding):
        if row[col_index] == col_value:
            yield row
