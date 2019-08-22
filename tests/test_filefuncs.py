from pathlib import Path
import shutil
import os
import pytest
import zipfile
from utilfuncs import filefuncs

from utilfuncs.filefuncs import (
    move_file,
    move_files,
    move_dir,
    move_files_based_on_text,
    # get_file_paths_by_substr,
    filter_by_glob,
)


def getSrc():
    p = Path(__file__).absolute()
    src = p.parent / "files"
    return src


def getDest():
    p = Path(__file__).absolute()
    dest = p.parent
    return dest


def test_move_file_doesnt_move_if_src_is_dir(mocker):
    src = getSrc()
    dest = getDest()

    mocker.patch("shutil.move")

    move_file(src, dest)

    assert shutil.move.call_count == 0


def test_move_file_works_if_src_is_file(mocker):
    src = getSrc()
    src = src.joinpath("Employee.csv")
    dest = getDest()

    mocker.patch("shutil.move")

    move_file(src, dest)

    print(src)
    print(dest)

    assert shutil.move.call_count == 1


def test_move_files_moves_all_files_without_ext(mocker):
    src = getSrc()
    dest = getDest()

    num_files = len(os.listdir(src))

    mocker.patch("shutil.move")

    move_files(src, dest)

    assert shutil.move.call_count == num_files


def test_move_files_moves_all_files_with_ext(mocker, tmp_path):
    dest = getDest()

    files = [
        "a.csv",
        "b.csv",
        "c.txt"
    ]
    for f in files:
        open(tmp_path / f, "w").write("\n")

    mocker.patch("shutil.move")

    move_files(tmp_path, dest, ".txt")

    assert shutil.move.call_count == 1


def test_move_files_based_on_text(mocker):
    src = getSrc()
    dest = getDest()

    mocker.patch("shutil.move")

    move_files_based_on_text(src, dest, "_erROR_", False)


def test_move_dir(mocker):
    src = getSrc()
    dest = getDest()

    mocker.patch("shutil.move")

    move_dir(src, dest)


def test_filter_by_glob_works():
    myList = [
        "hulk_smash.txt",
        "hulk_smash.log",
        "hulk_sleep.txt"
    ]

    pattern = "hulk_*.txt"

    expected = [
        "hulk_smash.txt",
        "hulk_sleep.txt"
    ]

    result = filter_by_glob(myList, pattern)
    print(result)

    assert expected == result


def test_filter_by_glob_works_v1():
    myList = [
        "newyork_liberty",
        "newyork_empire",
        "newyork_liberty"
    ]

    pattern = "*_liberty"

    expected = [
        "newyork_liberty",
        "newyork_liberty"
    ]

    result = filter_by_glob(myList, pattern)
    print(result)

    assert expected == result


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
