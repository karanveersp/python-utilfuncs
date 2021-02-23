import os
import pytest
import zipfile
from pathlib import Path
from unittest.mock import patch

import utilfuncs as util


def create_dest(tmpdir):
    dest = Path(tmpdir) / "dest"
    dest.mkdir()
    return dest


def build_dummy_files(tmpdir, file_names):
    files = [Path(tmpdir) / f for f in file_names]
    [f.write_text("_") for f in files]
    return files

# TODO: Fix
def test_get_file_with_string_in_name_works(tmpdir):
    dummies = build_dummy_files(tmpdir, ["file_a.txt", "file_b.txt", "file_aabb.txt"])

    files = util.get_files_where_string_in_name(tmpdir, "a", isSensitive=True)

    assert sorted(files) == [dummies[0], dummies[2]]


@patch("shutil.move")
def test_move_file_doesnt_move_if_src_is_dir(mock_move, tmpdir):
    dest = create_dest(tmpdir)

    util.move_file(tmpdir, dest)

    mock_move.assert_not_called()


def test_move_file_works_if_src_is_file(tmpdir):
    src = Path(tmpdir) / "a.txt"
    src.write_text("_")
    dest = create_dest(tmpdir)

    util.move_file(src, dest)

    assert (dest / "a.txt").is_file()


def test_move_files_moves_all_files_without_ext(tmpdir):
    build_dummy_files(tmpdir, ["a.txt", "b.log", "c.csv"])
    dest = create_dest(tmpdir)

    util.move_files(tmpdir, dest)

    assert all([(dest / name).is_file() for name in os.listdir(dest)])


def test_move_files_moves_all_files_with_ext(tmpdir):
    dest = create_dest(tmpdir)
    build_dummy_files(tmpdir, ["a.txt", "b.txt", "c.log"])

    util.move_files(tmpdir, dest, ".txt")

    assert not (dest / "c.log").is_file()
    assert (dest / "a.txt").is_file()
    assert (dest / "b.txt").is_file()


def test_move_files_based_on_text_not_case_sensitive(tmpdir):
    build_dummy_files(tmpdir, ["a.txt", "b_error_.txt", "c.txt"])
    dest = create_dest(tmpdir)

    util.move_files_where_string_in_name(tmpdir, dest, "_erROR_", isSensitive=False)

    assert (dest / "b_error_.txt").is_file()
    assert not (dest / "a.txt").is_file()
    assert not (dest / "c.txt").is_file()


def test_move_dir(tmpdir):
    src = Path(tmpdir) / "some_dir"
    src.mkdir()
    dest = create_dest(tmpdir)

    util.move_dir(src, dest)

    assert (dest / "some_dir").is_dir()
    assert not src.is_dir()


def test_filter_by_glob_works():
    my_list = ["hulk_smash.txt", "hulk_smash.log", "hulk_sleep.txt"]

    pattern = "hulk_*.txt"

    expected = ["hulk_smash.txt", "hulk_sleep.txt"]

    result = util.filter_by_glob(my_list, pattern)

    assert expected == result


def test_filter_by_glob_works_v1():
    my_list = ["newyork_liberty", "newyork_empire", "newyork_liberty"]

    pattern = "*_liberty"

    expected = ["newyork_liberty", "newyork_liberty"]

    result = util.filter_by_glob(my_list, pattern)

    assert expected == result


def test_zipdir_works(tmp_path):
    # Arrange - create a directory with a file in tmp_path
    source_dir = tmp_path / "mydir"
    somefile = source_dir / "myfile.txt"
    os.mkdir(source_dir)
    with open(somefile, "w") as myfile:
        myfile.write("Some content")

    # Act
    zip_path = util.zipdir(source_dir, "myarchive")
    print(str(zip_path))

    # Assert
    assert zip_path.is_file()


def test_value_error_if_source_dir_doesnt_exist(tmp_path):
    with pytest.raises(ValueError):
        # Arrange
        source_dir = tmp_path / "mydir"
        # Act
        util.zipdir(source_dir, "myarchive")


def test_zipfiles_works(tmp_path):
    # Arrange  - create 3 files with one file in a separate directory
    os.mkdir(tmp_path / "somedir")
    files = build_dummy_files(tmp_path, ["a.txt", "b.txt", "c.txt"])

    dest_dir = tmp_path

    # Act
    zip_path = util.zipfiles(files, dest_dir, "files_archive")

    # Assert
    assert zip_path.is_file()

    with zipfile.ZipFile(zip_path, "r") as z:
        # all files are at the top level in the zip - no dirs
        assert sorted(z.namelist()) == ["a.txt", "b.txt", "c.txt"]


def test_file_conversion_to_utf8_works(tmpdir):
    # Arrange
    filepath = Path(tmpdir) / "encode_test.csv"
    windows_1252_text = u"\u20AC\u2020\u2020"
    filepath.write_bytes(windows_1252_text.encode("windows-1252"))

    # Act
    converted_file = util.convert_to_utf8(filepath, Path(tmpdir))

    # Assert
    assert converted_file.is_file()
    with open(converted_file, "rb") as f:
        content_bytes = f.read()
        assert windows_1252_text == content_bytes.decode("utf-8")


def test_rename_file_works(tmpdir):
    # arrange
    test_file = Path(tmpdir / "test.log")
    with open(test_file, 'w') as f:
        f.write("Some data")
    new_name = "test__ERROR__"  # appending error to log name

    # act
    renamed_file = util.rename_file(test_file, new_name)

    # assert
    assert not Path(test_file).is_file()
    assert renamed_file.is_file()


def test_create_dir_if_not_exists_works(tmpdir):
    # arrange
    test_dirs = Path(tmpdir / "dir1" / "dir2")

    # act
    util.create_dir_if_not_exists(test_dirs)

    # assert
    assert test_dirs.is_dir()
