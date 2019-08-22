from pathlib import Path
import os
import shutil


def zipdir(source_dir, zipname=None):
    """
    Creates a zip archive which contains the directory specified in dirPath.

    Args:
        source_dir: Path or str representing absolute directory path
        zipname (str, optional): Name of the generated archive. If not
            provided, the name defaults to the directory's name.

    Returns:
        Path for the zip archive created in the source_dir's parent dir
    """
    source = Path(source_dir)

    if not source.is_dir():
        raise ValueError(f"{source} is not a valid directory")

    dest = source.parent

    # chdir to create the zip in the parent dir
    os.chdir(dest)

    if zipname is None:
        zipname = source.name
    print("zipname: " + zipname)

    shutil.make_archive(zipname, format="zip", root_dir=source)

    return dest.joinpath(zipname + ".zip")


def zipfiles(file_paths, dest_dir, zipname):
    """
    Creates a zip archive from list of file paths in destination.

    Args:
        file_paths: List of Path objects or strings
        dest_dir: Path to directory where zip will be generated
        zipname: Name of the zip archive

    Returns:
        Path for the zip archive created
    """
    # convert to Path objects
    dest = Path(dest_dir)
    files = [Path(f) for f in file_paths]

    if not dest.is_dir():
        raise ValueError(f"{dest} is not a valid directory")

    os.chdir(dest)

    # copy all files in the list to a temp dir in dest
    temp_dir = dest / "temp"
    if temp_dir.is_dir():
        shutil.rmtree(temp_dir)
    os.mkdir(temp_dir)

    for f in files:
        shutil.copyfile(f, temp_dir / f.name)

    shutil.make_archive(zipname, format="zip", root_dir=temp_dir)

    shutil.rmtree(temp_dir)

    return dest.joinpath(zipname + ".zip")
