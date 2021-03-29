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


def test_move_file_works(tmpdir):
    src = Path(tmpdir) / "a.txt"
    src.write_text("_")
    dest = create_dest(tmpdir)

    util.move_file(src, dest)

    content = (dest / "a.txt").read_text()
    assert content == "_"


def test_move_files_moves_all_files_without_ext(tmpdir):
    build_dummy_files(tmpdir, ["a.txt", "b.log", "c.csv"])
    dest = create_dest(tmpdir)

    util.move_files(tmpdir, dest)

    assert all([(dest / name).is_file() for name in os.listdir(dest)])


def test_move_files_works_on_specified_extensions(tmpdir):
    dest = create_dest(tmpdir)
    build_dummy_files(tmpdir, ["a.txt", "b.txt", "c.log"])

    util.move_files(tmpdir, dest, ".txt")

    assert not (dest / "c.log").is_file()
    assert (dest / "a.txt").is_file()
    assert (dest / "b.txt").is_file()


def test_move_files_matching_regex_works(tmpdir):
    build_dummy_files(tmpdir, ["a.txt", "b_error_.txt", "c.txt"])
    dest = create_dest(tmpdir)

    util.move_files_matching_regex(tmpdir, dest, "*_error_*")

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


def test_zipdir_works(tmp_path):
    # Arrange - create a directory with a file in tmp_path
    source_dir = tmp_path / "mydir"
    somefile = source_dir / "myfile.txt"
    os.mkdir(source_dir)
    somefile.write_text("Some content")

    # Act
    zip_path = util.zipdir(source_dir)

    # Assert
    assert zip_path.is_file()


def test_invalid_dir_error_if_dir_doesnt_exist(tmp_path):
    with pytest.raises(util.InvalidDirectoryPath):
        # Arrange
        source_dir = tmp_path / "mydir"
        # Act
        util.zipdir(source_dir, "myarchive")


def test_zipfiles_works(tmp_path):
    # Arrange  - create 3 files
    files = build_dummy_files(tmp_path, ["a.txt", "b.txt", "c.txt"])
    zip_path = tmp_path / "files_archive.zip"
    # Act
    util.zipfiles(zip_path, files)

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
    contents = util.get_contents_as_utf8(filepath)

    # Assert
    assert windows_1252_text == contents.decode("utf-8")


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
