import os
import shutil
import re
import ast


def organize_apps(base_dir, dest_dir):
    """
    Organizes app directories within the base directory based on app versions, categories, price, assets, and authors.

    Args:
        base_dir (str): Path to the base directory containing app directories.
        dest_dir (str): Path to the destination directory where organized app directories will be placed.
    """
    count_apps = 0
    for dirpath, dirnames, filenames in os.walk(base_dir):
        if "__manifest__.py" in filenames or "__openerp__.py" in filenames:  # Identify app directory
            manifest_file = os.path.join(dirpath, "__manifest__.py") if "__manifest__.py" in filenames else os.path.join(dirpath, "__openerp__.py")
            # Read the manifest file and extract the version, category, price, assets, and author
            with open(manifest_file, "r") as file:
                manifest_content = file.read()
                manifest_content = ''.join(c for c in manifest_content if ord(c) < 128)
                version_match = re.search(r"['\"]version['\"]\s*:\s*['\"](\d+)", manifest_content)

                version = version_match.group(1) if version_match else '0.1'

                try:
                    count_apps += 1
                    print('dirpath',dirpath)
                    manifest_dict = ast.literal_eval(manifest_content)
                    category = re.sub(r'[^\w\s]+', '-', manifest_dict.get('category', 'NoCategory').replace(",", " and ").lower())
                    price = 'Paid' if manifest_dict.get('price') and int(manifest_dict.get('price')) > 0 else 'Free'
                    assets = 'Assets' if manifest_dict.get('assets') and isinstance(manifest_dict.get('assets'), dict) and manifest_dict.get('assets') else 'NoAssets'
                    author = manifest_dict.get('author', 'NoAuthor')
                    if isinstance(author, list):
                        author = ', '.join(author)
                    if isinstance(author, str):
                        author = re.sub(r'[^\w\s]+', '-', author.replace(",", " and "))
                except ValueError:
                    category = 'NoCategory'
                    price = 'Free'
                    assets = 'NoAssets'
                    author = 'NoAuthor'

                version_dir = os.path.join(dest_dir, version)
                category_dir = os.path.join(version_dir, category)
                price_dir = os.path.join(category_dir, price)
                assets_dir = os.path.join(price_dir, assets)
                final_dir = os.path.join(assets_dir, author)
                os.makedirs(final_dir, exist_ok=True)
                # "Next in this task move the app directory if condition is true to new folder called duplicated_apps"

                # Check if the app directory already exists in the author directory
                app_dir_name = os.path.basename(dirpath)
                new_dir_path = os.path.join(final_dir, app_dir_name)

                # If the directory already exists, create a new directory named "copy_1" inside the existing directory
                copy_count = 1
                while os.path.exists(new_dir_path):
                    new_dir_path = os.path.join(final_dir, f'copy_{copy_count}', app_dir_name)
                    copy_count += 1

                # Move the app directory to the new unique directory
                os.makedirs(new_dir_path, exist_ok=True)
                shutil.move(dirpath, new_dir_path)
    print('count_apps', count_apps)
if __name__ == "__main__":
    base_dir = "/home/amr/PycharmProjects/OLD - PycharmProjects/odoo16/addons"
    dest_dir = "/home/amr/PycharmProjects/organized_apps"
    organize_apps(base_dir, dest_dir)