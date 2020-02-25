import os
import shutil
import datetime
from pathlib import Path


def create_dir_if_not_exists(dirpath):
    """Creates a directory and all intermediate directories if they don't exist"""
    if not Path(dirpath).is_dir() and "." not in str(dirpath):
        os.makedirs(dirpath, exist_ok=True)


def rename_file(filepath, new_name):
    """
    Rename the given file with new name.
    Extension remains the same.
    Returns path to renamed file.
    """
    name, ext = Path(filepath).name.split(".")
    name_with_ext = new_name + f".{ext}"
    renamed_file_path = Path(filepath).parent / name_with_ext
    os.replace(filepath, renamed_file_path)
    return renamed_file_path


def move_file(src_file, dest_dir):
    """Moves src file to dest dir"""
    if Path(src_file).is_file():
        shutil.move(str(src_file), str(dest_dir))


def move_files(src, dest, ext=""):
    """Moves all files of one extension from src to dest"""
    filenames = os.listdir(src)
    for name in filenames:
        filepath = Path(src) / name
        if name.endswith(ext) and filepath.is_file():
            destpath = Path(dest) / filepath.name
            shutil.move(str(filepath), str(destpath))


def move_dir(src, dest):
    """Moves dir from source to destination"""
    if Path(src).is_dir():
        shutil.move(str(src), str(dest))


def move_files_where_string_in_name(src, dest, string, isSensitive):
    """
    Moves multiple files from one folder to the other based on text characters in file name
    """
    filenames = os.listdir(str(src))
    for name in filenames:
        filepath = Path(src) / name
        destpath = Path(dest) / filepath.name
        if isSensitive:
            if string in name:
                shutil.move(str(filepath), str(destpath))
        else:
            if string.upper() in name.upper():
                shutil.move(str(filepath), str(destpath))


def get_files_where_string_in_name(dirpath, string, isSensitive):
    """
    Gets list of file paths in a directory based on text characters in file name
    """
    fpaths = [str(x) for x in os.listdir(dirpath)]
    retval = []
    for name in fpaths:
        if isSensitive:
            if string in name:
                retval.append(name)
        else:
            if string.upper() in name.upper():
                retval.append(name)
    return [dirpath / name for name in retval]


def filter_by_glob(collection, pattern):
    """
    Returns a filtered collection based on which
    items match the provided string pattern.
    """
    parts = pattern.split("*")
    beginning = parts[0]
    ending = parts[1]

    new_list = []

    for item in collection:
        item_as_str = str(item)
        if item_as_str.startswith(beginning) and item_as_str.endswith(ending):
            new_list.append(item)
    return new_list


def zipdir(source_dir, zipname=None):
    """
    Creates a zip archive which contains the directory specified in dirPath.

    Args:
        source_dir: Path or str representing absolute directory path
        zipname (str, optional): Name of the generated archive. If not
            provided, the name defaults to the directory's name.

    Returns:
        Path for the zip archive created in the source_dir's parent dir

    Raises:
        ValueError if source is an invalid directory
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

    Raises:
        ValueError if dest dir is invalid
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


def convert_to_utf8(filepath, target_dir):
    import chardet
    import codecs

    filepath = Path(filepath)

    with open(filepath, "rb") as f:
        content_bytes = f.read()
        detected = chardet.detect(content_bytes)
        file_encoding = detected["encoding"]
        # print(f"{filepath}: detected as {file_encoding}."
        if "utf-8" in file_encoding.lower():
            return filepath
        elif file_encoding is None:
            content_text = codecs.decode(content_bytes)
        else:
            content_text = codecs.decode(content_bytes, file_encoding, errors="replace")

    name, ext = filepath.name.split(".")
    encoded_file_name = f"{name}-utf-8.{ext}"

    with open(target_dir / encoded_file_name, "wb") as f:
        f.write(codecs.encode(content_text, "utf-8", errors="replace"))
        # print(f"{encoded_file_name} written to")

    return target_dir / encoded_file_name


def all_files_under(path, extension=""):
    """
    Iterates through all files that are under the given path with the given extension ex '.log'

    Args:
        path: The directory to scan
        extension (str, optional): The extensions to consider if provided (with period)
    Returns:
        List of Path objects or empty list if no files in directory
    """
    results = []

    try:
        currpath, _, filenames = next(os.walk(path))  # only traverse one level
    except StopIteration:
        # means no files in log folder
        return results

    for name in filenames:
        if extension in name:  # empty string extension will match all files
            results.append(Path(currpath) / name)

    return results


def delete_old_files(dirpath, extension="", days=1):
    """
    Deletes files older than a certain number of days.

    Args:
        dirpath: Path for directory
        extension (str, optional): File extension
        days (int, optional): Number of days for file age
    """
    numberOfDays = -1 * days
    days_ago = datetime.datetime.now() + datetime.timedelta(numberOfDays)

    dirpath = Path(dirpath)

    filepaths = all_files_under(dirpath, extension)

    for f in filepaths:
        fpath = Path(f)
        last_m_time = datetime.datetime.fromtimestamp(fpath.stat().st_mtime)
        if last_m_time < days_ago:
            os.remove(fpath)
