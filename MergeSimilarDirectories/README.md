# Merge Similar Directories

This Python script is designed to merge directories that are similar in a given directory structure. It's particularly useful when you have multiple directories with similar content and you want to consolidate them into a single directory.

## How it works

The script walks through the directory structure of the specified main directory. For each directory, it checks if there is a `__manifest__.py` file. If such a file is found, the directory is grouped by its first level directory. 

After grouping, the script merges the directories in each group. It moves all files from the child directories to the first level directory. If a file with the same name exists in the first level directory, the script renames the file to avoid overwriting.

## Usage

1. Replace the `main_dir` variable in the `if __name__ == "__main__":` section with the path to your main directory.
2. Run the script with Python.

```python
main_dir = "your_directory_path"
merge_directories(main_dir)
```

## Requirements

- Python 3
- `os`, `shutil`, and `collections` modules (standard in Python 3)

## Note

Please use this script with caution. It's recommended to backup your files before running the script.