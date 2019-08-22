from pathlib import Path
import pytest

from utilfuncs import csvfuncs


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
    rows = [row for row in csvfuncs.get_rows(csvfile)]
    print(rows)

    assert (
        rows[0] == ["FirstName", "LastName", "Email"]
        and rows[1] == ["Chris", "Redfield", "chris@gmail.com"]
        and rows[2] == ["Albert", "Whesker", "albert@gmail.com"]
    )


def test_raises_file_not_found_error_for_missing_file():
    with pytest.raises(FileNotFoundError):
        next(csvfuncs.get_rows(Path("C:/abc.csv")))


def test_csv_file_can_be_written(tmp_path):
    # Arrange
    csvpath = tmp_path / "outfile.csv"
    list_of_rows = [["a", "b", "c", "d"], ["e", "f", "g", "h"]]

    # Act
    csvfuncs.write_rows(csvpath, list_of_rows)

    # Assert
    assert (
        Path.is_file(csvpath)
        and next(csvfuncs.get_rows(csvpath)) == list_of_rows[0]
    )


def test_row_is_appended_to_existing_csv(tmp_path):
    # Arrange
    csvfile = tmp_path / "fileToAppend.csv"
    csvfuncs.write_rows(csvfile, [[1, 2, 3, 4]])
    row_to_append = [5, 6, 7, 8]

    # Act
    csvfuncs.append_row(csvfile, row_to_append)

    # Assert
    # read all rows from csvfile
    rows = [row for row in csvfuncs.get_rows(csvfile)]
    assert len(rows) == 2
