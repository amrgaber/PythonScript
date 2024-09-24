# addon_structure.py

import os
import sys
import pyperclip

# List of files and directories to ignore
IGNORE_LIST = [
    '.git', '.gitignore', '__pycache__', '.idea', '.vscode',
    '*.pyc', '*.pyo', '*.mo', '*.pot', '*.log', '*.bak',
    '.DS_Store', 'Thumbs.db', 'desktop.ini',
    'node_modules', 'package-lock.json', 'yarn.lock',
    '.editorconfig', '.eslintrc.js', '.prettierrc',
    'LICENSE', 'README.md', 'CHANGELOG.md', 'CONTRIBUTING.md'
]

def should_ignore(name):
    return any(
        ignored_item in name or
        (ignored_item.startswith('*') and name.endswith(ignored_item[1:]))
        for ignored_item in IGNORE_LIST
    )

def print_directory_structure(startpath, level=0):
    structure = []
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if not should_ignore(d)]
        level = root.replace(startpath, '').count(os.sep)
        indent = '    ' * level
        structure.append(f'{indent}{os.path.basename(root)}/')
        subindent = '    ' * (level + 1)
        for f in files:
            if not should_ignore(f):
                structure.append(f'{subindent}{f}')
    return '\n'.join(structure)

def main():
    if len(sys.argv) > 1:
        addon_path = sys.argv[1]
    else:
        addon_path = input("Enter the path to your Odoo addon: ").strip()

    if not os.path.isdir(addon_path):
        print("Error: The provided path is not a valid directory.")
        return

    structure = print_directory_structure(addon_path)
    print("\nAddon Structure:")
    print(structure)

    try:
        pyperclip.copy(structure)
        print("\nThe addon structure has been copied to your clipboard.")
    except:
        print("\nUnable to copy to clipboard. You may need to install 'pyperclip' or copy manually.")

if __name__ == "__main__":
    main()