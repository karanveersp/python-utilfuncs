import pytest
import os
import zipfile

from utilfuncs import filefuncs


def test_zipdir_works(tmp_path):
    # Arrange - create a directory with a file in tmp_path
    source_dir = tmp_path / "mydir"
    somefile = source_dir / "myfile.txt"
    os.mkdir(source_dir)
    with open(somefile, "w") as myfile:
        myfile.write("Some content")

    # Act
    zip_path = filefuncs.zipdir(source_dir, "myarchive")
    print(str(zip_path))

    # Assert
    assert zip_path.is_file()


def test_value_error_if_source_dir_doesnt_exist(tmp_path):
    with pytest.raises(ValueError):
        # Arrange
        source_dir = tmp_path / "mydir"
        # Act
        filefuncs.zipdir(source_dir, "myarchive")


def test_zipfiles_works(tmp_path):
    # Arrange  - create 3 files with one file in a separate directory
    os.mkdir(tmp_path / "somedir")
    files = [
            tmp_path / "a.txt",
            tmp_path / "somedir" / "b.txt",
            tmp_path / "c.txt"
    ]
    for f in files:
        with open(f, "wt") as file:
            file.write("content")

    dest_dir = tmp_path

    # Act
    zip_path = filefuncs.zipfiles(files, dest_dir, "files_archive")

    # Assert
    assert zip_path.is_file()

    with zipfile.ZipFile(zip_path, "r") as z:
        # all files are at the top level in the zip - no dirs
        assert z.namelist() == ["a.txt", "b.txt", "c.txt"]
