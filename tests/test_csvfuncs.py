from pathlib import Path

from utilfuncs import csvfuncs

class TestCsvFuncs():
    testDir = Path(__file__).parent / "files"

    def test_csv_file_can_be_read(self):
        # Arrange
        csvFile = self.testDir / "Employee.csv"

        # Act
        rows = [row for row in csvfuncs.get_rows(csvFile)]

        assert (
            rows[0] == ["FirstName", "LastName", "Email"]
            and rows[1] == ["John", "Doe", "jdoe@gmail.com"]
            and rows[2] == ["Albert", "Whesker", "aw@gmail.com"]
        )


    def test_csv_file_can_be_written(self):
        # Arrange
        csvpath = self.testDir / "outfile.csv"
        list_of_rows = [
            ["a", "b", "c", "d"],
            ["e", "f", "g", "h"]
        ]

        # Act
        csvfuncs.write_rows(csvpath, list_of_rows)

        # Assert
        assert (
            Path.is_file(csvpath)  # file exists
            and next(csvfuncs.get_rows(csvpath)) == list_of_rows[0]  # first row matches
        )

    
    def test_row_is_appended_to_existing_csv(self):
        # Arrange
        csvfile = self.testDir / "fileToAppend.csv"
        csvfuncs.write_rows(csvfile, [[1, 2, 3, 4]])
        row_to_append = [5, 6, 7, 8]

        # Act
        csvfuncs.append_row(csvfile, row_to_append)

        # Assert
        # read all rows from csvfile
        rows = [row for row in csvfuncs.get_rows(csvfile)]
        assert len(rows) == 2
            