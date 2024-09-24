import os
import re
from typing import List, Dict, Any

IGNORED_DIRS = {
    '__pycache__', 'node_modules', '.git', '.idea', '.vscode',
    'static/lib', 'static/src/lib'
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
        'other_files': []
    }

    for root, dirs, files in os.walk(addon_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for file in files:
            if file in IGNORED_FILES or any(file.endswith(ext) for ext in IGNORED_EXTENSIONS):
                continue

            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, addon_path)

            if file == '__manifest__.py':
                structure['manifest'] = relative_path
            elif relative_path.startswith('models/'):
                structure['models'].append(relative_path)
            elif relative_path.startswith('views/'):
                structure['views'].append(relative_path)
            elif relative_path.startswith('controllers/'):
                structure['controllers'].append(relative_path)
            elif relative_path.startswith('wizards/') or relative_path.startswith('wizard/'):
                structure['wizards'].append(relative_path)
            elif relative_path.startswith('reports/') or relative_path.startswith('report/'):
                structure['reports'].append(relative_path)
            elif relative_path.startswith('security/'):
                structure['security'].append(relative_path)
            elif relative_path.startswith('data/'):
                structure['data'].append(relative_path)
            elif relative_path.startswith('demo/'):
                structure['demo'].append(relative_path)
            elif relative_path.startswith('i18n/'):
                structure['i18n'].append(relative_path)
            elif relative_path.startswith('static/'):
                structure['static'].append(relative_path)
            elif relative_path.startswith('lib/'):
                structure['lib'].append(relative_path)
            elif relative_path.startswith('tests/'):
                structure['tests'].append(relative_path)
            else:
                structure['other_files'].append(relative_path)

    return structure

def generate_report(addon_structure: Dict[str, Any]) -> str:
    report = f"Addon: {addon_structure['name']}\n\n"

    if addon_structure['manifest']:
        report += f"Manifest: {addon_structure['manifest']}\n\n"
    else:
        report += "Warning: No manifest file found.\n\n"

    for section, files in addon_structure.items():
        if section in ['name', 'manifest']:
            continue
        if files:
            report += f"{section.capitalize()}:\n"
            for file in sorted(files):
                report += f"  - {file}\n"
            report += "\n"

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

    for addon in addons:
        report = generate_report(addon)
        print(report)
        print("-" * 80)

if __name__ == "__main__":
    main()