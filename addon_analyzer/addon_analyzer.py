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
        'init': None,
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
        dirs[:] = [d for d in dirs if d.lower() not in IGNORED_DIRS]

        for file in files:
            if file.lower() in IGNORED_FILES or any(file.lower().endswith(ext) for ext in IGNORED_EXTENSIONS):
                continue

            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, addon_path)
            content = read_file_content(file_path)

            file_info = {
                'path': relative_path,
                'content': content
            }

            if file.lower() == '__manifest__.py':
                structure['manifest'] = file_info
            elif file.lower() == '__init__.py' and relative_path.lower() == '__init__.py':
                structure['init'] = file_info
            else:
                categorized = False
                for key in structure.keys():
                    if key in ['name', 'manifest', 'init']:
                        continue
                    if relative_path.lower().startswith(f"{key}/") or relative_path.lower().startswith(f"{key}s/"):
                        if key == 'doc':
                            print('********key', key,structure[key],file_info)
                        structure[key].append(file_info)
                        categorized = True
                        break
                if not categorized:
                    structure['other_files'].append(file_info)

    return structure


def generate_report(addon_structure: Dict[str, Any]) -> str:
    report = f"Addon: {addon_structure['name']}\n\n"

    if addon_structure['manifest']:
        manifest_info = addon_structure['manifest']
        report += f"Manifest: {manifest_info['path']}\n"
        report += "Content:\n```python\n"
        report += manifest_info['content']
        report += "\n```\n\n"
    else:
        report += "Warning: No manifest file found.\n\n"

    if addon_structure['init']:
        init_info = addon_structure['init']
        report += f"__init__.py:\n"
        report += "Content:\n```python\n"
        report += init_info['content']
        report += "\n```\n\n"

    section_order = [
        'models', 'views', 'controllers', 'wizards', 'reports', 'security',
        'data', 'demo', 'i18n', 'static', 'lib', 'tests', 'hooks', 'migrations',
        'doc', 'sample', 'backup', 'other_files'
    ]

    for section in section_order:
        files = addon_structure[section]
        if files:
            report += f"{section.capitalize()}:\n"
            for file_info in sorted(files, key=lambda x: x['path'].lower()):
                report += f"  File: {file_info['path']}\n"
                report += "  Content:\n```\n"
                report += file_info['content']
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
