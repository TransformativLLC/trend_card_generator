# IMPORTS
import yaml
from pathlib import Path


# PACKAGE MANAGEMENT
__all__ = [
    "load_config",
]


# FUNCTIONS
def load_config(filename: str, config_dir_name: str = "src/agents/config") -> dict:
    """
    Loads a YAML configuration file from a specified directory or its parent directories.

    This function searches for the configuration file in the current working directory
    and its parent directories under a folder named `config_dir_name`. When the file is
    found, it is parsed and returned as a dictionary. If the file does not exist in the
    specified directory hierarchy, a FileNotFoundError is raised.

    Args:
        filename: Name of the configuration file to load.
        config_dir_name: Name of the directory to search for the configuration file.
            Defaults to "config".

    Returns:
        dict: Parsed contents of the configuration file.

    Raises:
        FileNotFoundError: If the configuration file cannot be found in the specified
        directory or its parent directories.
    """
    current = Path.cwd()
    for parent in [current] + list(current.parents):
        config_dir = parent / config_dir_name
        if config_dir.exists():
            for file_path in config_dir.rglob(filename):
                with file_path.open('r', encoding='utf-8') as file:
                    return yaml.safe_load(file)
    raise FileNotFoundError(f"Config file '{filename}' not found in any subdirectory under 'config' directory.")
