import os
import shutil

def clean_directory_structure(dir_path):
    count_removed = 0
    for root, dirs, _ in os.walk(dir_path):
        for dir in dirs:
            sub_dir = os.path.join(root, dir)
            if os.path.isdir(sub_dir) and os.path.isdir(os.path.join(sub_dir, dir)):
                redundant_dir = os.path.join(sub_dir, dir)
                if "__manifest__.py" in os.listdir(redundant_dir) or "__openerp__.py" in os.listdir(redundant_dir):
                    for filename in os.listdir(redundant_dir):
                        shutil.move(os.path.join(redundant_dir, filename), sub_dir)
                        count_removed += 1
                    os.rmdir(redundant_dir)
    print("Removed {} redundant directories".format(count_removed))

if __name__ == "__main__":
    base_dir = "your_apps_directory_path"
    clean_directory_structure(base_dir)