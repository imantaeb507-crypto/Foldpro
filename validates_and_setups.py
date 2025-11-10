import shutil
from pathlib import Path
import os
import tempfile
import sys
from typing import Union, Tuple, List
import random
import platform

def exit():
    print("Thank you for considering FoldPro.")
    sys.exit()








def creates_folders(folder_list: List[str], dest: Path) -> List[Path]:
    created_folders = []

    for name in folder_list:
        new_folder = dest / name  # full path: destination + folder name

        # Append random 5-digit number if folder exists
        while new_folder.exists():
            rand_num = random.randint(10000, 99999)
            new_folder = dest / f"{name}{rand_num}"

        new_folder.mkdir(exist_ok=True)  # create folder
        created_folders.append(new_folder)

    return created_folders


def checks_permissions():                 
    print("Please type in the path(absolute or relative) to the folder that you wanna organize")
    # The following code exits so as to give the user another chance too input a permmisble path/input
    while True:
        user_input = Path(input('>'))
        if str(user_input) in ['e', 'exit', 'exit please']:
            exit()
            
        if not user_input.exists():
            print(f"The given path: '{user_input!s}' does not exist on your computer.\nPlease input a path that does or type 'e' to exit this program.")
            continue
        try:
            if not user_input.is_dir():
                print(f"The given path must lead to a folder. {user_input.name()} is not.\nPlease give a path leading to a folder or type 'e' to exit")
                continue
        except PermissionError:
            print(f"Foldpro needs access to {user_input.name()} in order to run properly. Please give it and then re-run the program.")
            sys.exit()
        break
    if access_checker(user_input):
    # Returns a valid folder path from user thats been converted to a Path object:
        return  user_input

    

def setups(p: Path) -> Tuple[List[Path], Path]:
    # Base name for the copy
    base_copy_name = f"{p.name}_copy"
    copied_version_path = p.parent / base_copy_name

    # Append random 3-digit numbers until a non-existing path is found
    while copied_version_path.exists():
        rand_num = random.randint(100, 999)
        copied_version_path = p.parent / f"{p.name}_copy{rand_num}"

    # Copy the folder
    shutil.copytree(p, copied_version_path, dirs_exist_ok=True)

    # Create subfolders inside the copied folder
    folders = creates_folders(
        ["Pictures", "Code Files", "Downloads From Terminal", "Others"], 
        copied_version_path
    )

    for file in copied_version_path.glob('*'):
        if file.is_file() and file.issymlink():
            file.unlink()

    return folders, copied_version_path



def validates_and_setups() -> Tuple[List[Path], Path]:
    original_folder_path = checks_permissions()
    main_data = setups(original_folder_path)

    
