# Directory Cleaner

This script is designed to clean up a directory structure by removing redundant directories. It's particularly useful for Odoo module directories.

## How it works

The script walks through the directory structure of the specified base directory. For each directory, it checks if there is a subdirectory with the same name that contains either a `__manifest__.py` or `__openerp__.py` file. If such a directory is found, all files within it are moved to the parent directory, and the now empty subdirectory is removed.

## Usage

1. Replace the `base_dir` variable in the `if __name__ == "__main__":` section with the path to your base directory.
2. Run the script with Python.

## Requirements

- Python 3
- `os` and `shutil` modules (standard in Python 3)

## Note

Please use this script with caution. It's recommended to backup your files before running the script.