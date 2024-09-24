import os
import shutil
import re
import ast
import argparse


def get_category(manifest_path):
    with open(manifest_path, 'r') as file:
        content = file.read().strip()
        if not content:
            return 'Uncategorized'
        try:
            manifest = ast.literal_eval(content)
            category = manifest.get('category', '').strip()
            if not category:
                return 'Uncategorized'
            return category
        except (SyntaxError, ValueError):
            print(
                f"Warning: {manifest_path} could not be parsed. May be a syntax issue.")
            return 'Uncategorized'


def format_category_name(category):
    # Replace non-alphanumeric characters with spaces, convert to lowercase, and capitalize each word
    category = re.sub(r'[^\w\s]', ' ', category)
    category = ' '.join(word.capitalize() for word in category.split())
    return category


def is_same_manifest(src_manifest_path, dest_manifest_path):
    with open(src_manifest_path, 'r') as src_file, open(dest_manifest_path, 'r') as dest_file:
        return src_file.read().strip() == dest_file.read().strip()


def organize_addons_by_category(base_dir, dest_dir):
    count_addons = 0
    for dirpath, dirnames, filenames in os.walk(base_dir):
        if '__manifest__.py' in filenames:
            manifest_path = os.path.join(dirpath, '__manifest__.py')
            category = get_category(manifest_path)
            category = format_category_name(category)

            category_dir = os.path.join(dest_dir, category)
            os.makedirs(category_dir, exist_ok=True)

            addon_name = os.path.basename(dirpath)
            new_dir_path = os.path.join(category_dir, addon_name)

            if os.path.exists(new_dir_path):
                existing_manifest_path = os.path.join(
                    new_dir_path, '__manifest__.py')
                if os.path.exists(existing_manifest_path) and is_same_manifest(manifest_path, existing_manifest_path):
                    print(f"Skipping duplicate module: {addon_name}")
                    continue

            copy_count = 1
            while os.path.exists(new_dir_path):
                new_dir_path = os.path.join(
                    category_dir, f'copy_{copy_count}', addon_name)
                copy_count += 1

            shutil.copytree(dirpath, new_dir_path)
            count_addons += 1

    print('Total addons organized:', count_addons)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Organize Odoo addons by category.')
    parser.add_argument('--base_dir', type=str,
                        help='Path to the main directory containing addons')
    parser.add_argument('--dest_dir', type=str,
                        help='Path to the destination directory where organized addons will be copied')

    args = parser.parse_args()

    base_dir = args.base_dir or input(
        'Enter the path to the main directory (default: /home/amr/PycharmProjects/Odoo17/custom/AlWafeen): ') or '/home/amr/PycharmProjects/Odoo17/custom/AlWafeen'
    dest_dir = args.dest_dir or input(
        'Enter the path to the destination directory (default: /home/amr/PycharmProjects/Odoo17/custom/AppsByCateg_V017/APPS_V017): ') or '/home/amr/PycharmProjects/Odoo17/custom/AppsByCateg_V017/APPS_V017'

    organize_addons_by_category(base_dir, dest_dir)
