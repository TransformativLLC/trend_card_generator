from pathlib import Path
from typing import List


__all__ = [
    "get_file_list",
    "read_file",
    "append_to_filename",
    "get_directory_safe_model_name"
]


def get_file_list(path: str, extension: str) -> List[str]:
    """Get a list of all files in the specified path with the given extension.

    Args:
        path: The directory path to search for files.
        extension: The file extension to filter by (e.g., '.txt', 'txt').

    Returns:
        A list of file paths (as strings) that match the extension.

    Raises:
        FileNotFoundError: If the specified path does not exist.
        NotADirectoryError: If the specified path is not a directory.

    Examples:
        >>> get_file_list('/path/to/dir', '.txt')
        ['/path/to/dir/file1.txt', '/path/to/dir/file2.txt']

        >>> get_file_list('/path/to/dir', 'py')
        ['/path/to/dir/script.py']
    """
    path_obj = Path(path)

    if not path_obj.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")

    if not path_obj.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {path}")

    # Ensure extension starts with a dot
    if not extension.startswith('.'):
        extension = f'.{extension}'

    # Get all files with the specified extension
    file_list = [str(file) for file in path_obj.rglob(f'*{extension}')]

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

    Examples:
        >>> content = read_file('/path/to/file.md')
        >>> print(content)
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

    # Create new filename with appended suffix
    new_filename = f"{stem}{separator}{suffix}{extension}"

    # Return the full path with new filename
    return str(path_obj.parent / new_filename)


translation_table = str.maketrans('.:-', '___')
def get_directory_safe_model_name(model_name: str) -> str:
     return model_name.translate(translation_table)