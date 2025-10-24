from pathlib import Path
from typing import List


__all__ = [
    "get_file_list",
    "read_file",
    "append_to_filename",
]


def get_file_list(path: str, extension: str, exclude_names_with: str = None) -> List[str]:
    """
    Fetches a list of all files with a specified extension from a given directory recursively.

    This function retrieves files from the provided directory whose file names
    match the specified extension. It can optionally exclude files containing
    a particular substring in their names.

    Args:
        path: The path to the directory where files are searched.
        extension: The file extension to match.
        exclude_names_with: An optional string; files containing this substring
            in their names will be excluded from the list.

    Raises:
        FileNotFoundError: If the specified path does not exist.
        NotADirectoryError: If the specified path is not a directory.

    Returns:
        List[str]: A list of file paths that match the criteria.
    """
    path_obj = Path(path)

    if not path_obj.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")

    if not path_obj.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {path}")

    # Ensure the extension starts with a dot
    if not extension.startswith('.'):
        extension = f'.{extension}'

    # Get all files with the specified extension
    file_list = [str(file) for file in path_obj.rglob(f'*{extension}')]

    # apply name filter if specified
    if exclude_names_with:
        file_list = [file for file in file_list if not exclude_names_with in file]

    return file_list


def read_file(file_path: str) -> str:
    """Read a file and return its contents as a string.

    Args:
        file_path: The path to the file to read.

    Returns:
        The contents of the file as a string.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        IOError: If there is an error when reading the file.
    """
    path_obj = Path(file_path)

    if not path_obj.exists():
        raise FileNotFoundError(f"File does not exist: {file_path}")

    with open(path_obj, 'r', encoding='utf-8') as file:
        content = file.read()

    return content


def append_to_filename(file_path: str, suffix: str, separator: str = "_") -> str:
    """Append a string to the end of a filename before the extension.

    Args:
        file_path: The full file path including filename and extension.
        suffix: The string to append to the filename.
        separator: The separator string to use between filename and suffix (default: "_").

    Returns:
        The modified file path with the suffix appended to the filename.

    Examples:
        >>> append_to_filename('/path/to/file.txt', 'backup')
        '/path/to/file_backup.txt'

        >>> append_to_filename('/path/to/document.pdf', 'v2', '-')
        '/path/to/document-v2.pdf'

        >>> append_to_filename('report.md', 'edited')
        'report_edited.md'
    """
    path_obj = Path(file_path)

    # Get the stem (filename without extension) and suffix (extension)
    stem = path_obj.stem
    extension = path_obj.suffix

    # Create a new filename with appended suffix
    new_filename = f"{stem}{separator}{suffix}{extension}"

    # Return the full path with the new filename
    return str(path_obj.parent / new_filename)
