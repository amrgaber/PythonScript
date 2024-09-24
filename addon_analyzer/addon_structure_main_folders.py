# addon_structure.py

import os
import sys
import pyperclip

# List of directories to ignore
IGNORE_LIST = [
  '.git', '__pycache__', '.idea', '.vscode',
  'node_modules',
]

def should_ignore(name):
  return name in IGNORE_LIST

def print_directory_structure(startpath, level=0):
  structure = []
  for root, dirs, files in os.walk(startpath):
      dirs[:] = [d for d in dirs if not should_ignore(d)]
      level = root.replace(startpath, '').count(os.sep)
      indent = '    ' * level
      structure.append(f'{indent}{os.path.basename(root)}/')
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
  print("\nAddon Directory Structure:")
  print(structure)

  try:
      pyperclip.copy(structure)
      print("\nThe addon directory structure has been copied to your clipboard.")
  except:
      print("\nUnable to copy to clipboard. You may need to install 'pyperclip' or copy manually.")

if __name__ == "__main__":
  main()

# Created/Modified files during execution:
# addon_structure.py