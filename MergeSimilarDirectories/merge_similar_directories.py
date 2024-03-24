import os
import shutil
from collections import defaultdict

def merge_directories(main_dir):
    dir_dict = defaultdict(list)

    # Group directories by first level directory if they contain a __manifest__.py file
    for root, dirs, files in os.walk(main_dir):
        if "__manifest__.py" in files:
            first_level_dir = os.path.join(main_dir, root.split(os.sep)[1])
            dir_dict[first_level_dir].append(root)

    # Merge directories in each group
    for first_level_dir, child_dirs in dir_dict.items():
        for child_dir in child_dirs:
            for filename in os.listdir(child_dir):
                src_file = os.path.join(child_dir, filename)
                dst_file = os.path.join(first_level_dir, filename)

                # If a file with the same name exists in the first level directory, rename the file
                if os.path.exists(dst_file):
                    base, extension = os.path.splitext(filename)
                    i = 1
                    while os.path.exists(dst_file):
                        new_name = f"{base}_{i}{extension}"
                        dst_file = os.path.join(first_level_dir, new_name)
                        i += 1

                shutil.move(src_file, dst_file)

            os.rmdir(child_dir)

if __name__ == "__main__":
    main_dir = "your_directory_path"
    merge_directories(main_dir)