from pathlib import Path
import pytest

import utilfuncs.csv as util


def test_csv_file_can_be_read(tmp_path):
    # Arrange - write csv to tmp_path
    csvfile = tmp_path / "Employees.csv"
    with open(csvfile, "w") as testfile:
        testfile.writelines(
            [
                "FirstName,LastName,Email\n",
                "Chris,Redfield,chris@gmail.com\n",
                "Albert,Whesker,albert@gmail.com\n",
            ]
        )

    # Act
    rows = [row for row in util.get_rows(csvfile)]
    print(rows)

    assert (
        rows[0] == ["FirstName", "LastName", "Email"]
        and rows[1] == ["Chris", "Redfield", "chris@gmail.com"]
        and rows[2] == ["Albert", "Whesker", "albert@gmail.com"]
    )


def test_raises_file_not_found_error_for_missing_file():
    with pytest.raises(FileNotFoundError):
        next(util.get_rows(Path("C:/abc.csv")))


def test_csv_file_can_be_written(tmp_path):
    # Arrange
    csvpath = tmp_path / "outfile.csv"
    list_of_rows = [["a", "b", "c", "d"], ["e", "f", "g", "h"]]

    # Act
    util.write_rows(csvpath, list_of_rows)

    # Assert
    assert Path.is_file(csvpath) and next(util.get_rows(csvpath)) == list_of_rows[0]


def test_row_is_appended_to_existing_csv(tmp_path):
    # Arrange
    csvfile = tmp_path / "fileToAppend.csv"
    util.write_rows(csvfile, [[1, 2, 3, 4]])
    row_to_append = [5, 6, 7, 8]

    # Act
    util.append_row(csvfile, row_to_append)

    # Assert
    # read all rows from csvfile
    rows = [row for row in util.get_rows(csvfile)]
    assert len(rows) == 2


def test_get_rows_by_column_filter_works(tmp_path):
    # Arrange
    csvfile = Path(tmp_path) / "file.csv"
    util.write_rows(csvfile, [
        ["A", 1],
        ["B", 2],
        ["B", 3],
        ["A", 5],
        ["C", 0]
    ])

    # Act
    rows_for_B = [row for row in util.get_rows_by_column_filter(csvfile, col_index=0, col_value="B")]
    rows_for_A = [row for row in util.get_rows_by_column_filter(csvfile, 0, "A")]
    rows_for_C = [row for row in util.get_rows_by_column_filter(csvfile, 0, "C")]

    # Assert
    assert rows_for_B == [["B", '2'], ["B", '3']]
    assert rows_for_A == [["A", "1"], ["A", "5"]]
    assert rows_for_C == [["C", "0"]]
