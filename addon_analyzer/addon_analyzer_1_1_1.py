import os
import re
from typing import List, Dict, Any

IGNORED_DIRS = {
  '__pycache__', 'node_modules', '.git', '.idea', '.vscode',
  'static/lib', 'static/src/lib', 'external', 'min', 'templates'
}

IGNORED_FILES = {
  '.DS_Store', '.gitignore', 'package.json', 'package-lock.json',
  'README.md', 'LICENSE', '.eslintrc.js', '.babelrc', 'webpack.config.js'
}

IGNORED_EXTENSIONS = {
  '.pyc', '.pyo', '.mo', '.pot', '.log', '.bak', '.swp', '.csv', '.xls', '.xlsx', '.pdf'
}

IMPORTANT_FILES = {
  '__manifest__.py', '__init__.py', 'models/__init__.py', 'controllers/__init__.py',
  'wizards/__init__.py', 'reports/__init__.py', 'static/description/index.html'
}

def read_file_content(file_path: str) -> str:
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def analyze_addon(addon_path: str) -> Dict[str, Any]:
  addon_name = os.path.basename(addon_path)
  structure = {
      'name': addon_name,
      'manifest': None,
      'models': [],
      'views': [],
      'controllers': [],
      'wizards': [],
      'reports': [],
      'security': [],
      'data': [],
      'demo': [],
      'i18n': [],
      'static': [],
      'lib': [],
      'tests': [],
      'hooks': [],
      'migrations': [],
      'doc': [],
      'sample': [],
      'backup': [],
      'other_files': []
  }

  for root, dirs, files in os.walk(addon_path):
      dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

      for file in files:
          if file in IGNORED_FILES or any(file.endswith(ext) for ext in IGNORED_EXTENSIONS):
              continue

          file_path = os.path.join(root, file)
          relative_path = os.path.relpath(file_path, addon_path)
          content = read_file_content(file_path)

          file_info = {
              'path': relative_path,
              'content': content
          }

          if file == '__manifest__.py':
              structure['manifest'] = file_info
          elif relative_path.startswith('models/'):
              structure['models'].append(file_info)
          elif relative_path.startswith('views/'):
              structure['views'].append(file_info)
          elif relative_path.startswith(('controllers/', 'controller/')):
              structure['controllers'].append(file_info)
          elif relative_path.startswith(('wizards/', 'wizard/')):
              structure['wizards'].append(file_info)
          elif relative_path.startswith(('reports/', 'report/')):
              structure['reports'].append(file_info)
          elif relative_path.startswith('security/'):
              structure['security'].append(file_info)
          elif relative_path.startswith('data/'):
              structure['data'].append(file_info)
          elif relative_path.startswith('demo/'):
              structure['demo'].append(file_info)
          elif relative_path.startswith('i18n/'):
              structure['i18n'].append(file_info)
          elif relative_path.startswith('static/'):
              structure['static'].append(file_info)
          elif relative_path.startswith('lib/'):
              structure['lib'].append(file_info)
          elif relative_path.startswith('tests/'):
              structure['tests'].append(file_info)
          elif relative_path.startswith('hooks/'):
              structure['hooks'].append(file_info)
          elif relative_path.startswith('migrations/'):
              structure['migrations'].append(file_info)
          elif relative_path.startswith('doc/'):
              structure['doc'].append(file_info)
          elif relative_path.startswith('sample/'):
              structure['sample'].append(file_info)
          elif relative_path.startswith('backup/'):
              structure['backup'].append(file_info)
          else:
              structure['other_files'].append(file_info)

  return structure

def generate_report(addon_structure: Dict[str, Any]) -> str:
    report = f"Addon: {addon_structure['name']}\n\n"

    if addon_structure['manifest']:
        if isinstance(addon_structure['manifest'], dict):
            manifest_path = addon_structure['manifest'].get('path', 'Unknown path')
            manifest_content = addon_structure['manifest'].get('content', 'No content available')
        else:
            manifest_path = '__manifest__.py'
            manifest_content = str(addon_structure['manifest'])

        report += f"Manifest: {manifest_path}\n"
        report += "Content:\n```python\n"
        report += manifest_content
        report += "\n```\n\n"
    else:
        report += "Warning: No manifest file found.\n\n"

    for section, files in addon_structure.items():
        if section in ['name', 'manifest']:
            continue
        if files:
            report += f"{section.capitalize()}:\n"
            for file_info in sorted(files, key=lambda x: x['path'] if isinstance(x, dict) else x):
                if isinstance(file_info, dict):
                    file_path = file_info.get('path', 'Unknown path')
                    file_content = file_info.get('content', 'No content available')
                else:
                    file_path = file_info
                    file_content = 'Content not available'

                report += f"  File: {file_path}\n"
                report += "  Content:\n```\n"
                report += file_content
                report += "\n```\n\n"

    return report

def analyze_addons(addons_path: str) -> List[Dict[str, Any]]:
    addons = []
    for addon_name in os.listdir(addons_path):
        addon_path = os.path.join(addons_path, addon_name)
        if os.path.isdir(addon_path) and '__manifest__.py' in os.listdir(addon_path):
            addon_structure = analyze_addon(addon_path)
            addons.append(addon_structure)
    return addons


def main():
    addons_path = input("Enter the path to the Odoo addons directory: ")
    addons = analyze_addons(addons_path)

    # Create a new folder for the reports
    output_folder = f"{os.path.basename(addons_path)}_text"
    os.makedirs(output_folder, exist_ok=True)

    for addon in addons:
        report = generate_report(addon)
        addon_file_name = f"{addon['name']}_report.txt"
        addon_file_path = os.path.join(output_folder, addon_file_name)

        with open(addon_file_path, 'w', encoding='utf-8') as report_file:
            report_file.write(report)

    print(f"Reports have been saved in the '{output_folder}' directory.")

if __name__ == "__main__":
    main()