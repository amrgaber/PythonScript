import os
import zipfile

def extract_zip_files(main_folder):
    for root, dirs, files in os.walk(main_folder):
        for file in files:
            if file.endswith('.zip'):
                file_path = os.path.join(root, file)
                extract_dir = os.path.splitext(file_path)[0]
                if not os.path.isdir(extract_dir):
                    with zipfile.ZipFile(file_path, 'r') as zip_ref:
                        zip_ref.extractall(extract_dir)

if __name__ == "__main__":
    main_folder = "/home/amr/PycharmProjects/odoo_apps/Done/Accounting"  # Replace with your main folder path
    extract_zip_files(main_folder)