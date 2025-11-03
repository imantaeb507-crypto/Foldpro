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

def access_checker(p: Path):
    errors = []
    p = Path(p)
    # Helper functions for this function:
    def generate_random_strings():
        return [str(random.randint(0, 100)) for _ in range(10)]

    def _format_exception(e: Exception) -> str:
        #Return a short formatted exception message suitable for error logging.
        return f"{type(e).__name__}: {str(e)}"
    
    def _error_message_maker(list_of_errors: List[bool]) -> str:
        if users_os == "macOS":
            for error in list_of_errors:

            f'''
            Oops-looks like Foldpro has run into some issues with your computers filesystem.
            Read the following report if you wish to fix the issue.

            {list_of_errors}
            
            
            '''
    
        users_os = ""
        if platform.system() == "Darwin":
            users_os == "macOS"
        elif platform.system() == "Linux":
            users_os == "Linux"
        elif platform.system() == "Windows":
            users_os == "Linux"
        else:
            print(f"Foldpro cannot run on your {platform.system()}. It can only run on Linux, Windows or macOS using machines.")
            sys.exit()
        try:
            suffix0 = generate_random_strings()
            shutil.copytree(p, p.parent() / f"Foldpro_test_folder{suffix0}")
        except Exception as e:
            if users_os == "macOS":
                print("Foldpro could not create a copy of the given the directory. Please check the list of potential errors(and how too fix them) below if you wish to fix this issue.")
                print("1. Terminal does not have access to your filesystem.\nTo fix this navagate to the following: ' > System Settings > Privacy & Security > Full Disk Access' and toggle the terminal part to be on.")
                print("2. Disk is full and/or is read only. To fix this, make sure your computer has enough storage for the coped version and check the settings of the drive to make sure it is not read-only.")
                sys.exit()
            elif users_os == "Windows":
                print("Foldpro could not create a copy of the given directory. Please check the list of potential errors (and how to fix them) below if you wish to fix this issue.")
                print("1. Insufficient permissions to write to the destination folder.\n  To fix this, right-click the folder → Properties → Security, and ensure your user has 'Full Control', or run the program as an administrator.")
                print("2. Disk is full and/or is read-only.\n   To fix this, ensure the destination drive has enough free space and is not marked as read-only.")
                sys.exit()
            elif users_os == "Linux":
                print("Foldpro could not create a copy of the given directory. Please check the list of potential errors (and how to fix them) below if you wish to fix this issue.")
                print("1. Insufficient permissions to write to the destination folder.\n   To fix this, check folder ownership and permissions (`ls -ld <folder>`), and use `chmod`/`chown` as needed or run with proper user privileges.")
                print("2. Disk is full and/or is read-only.\n   To fix this, ensure the destination drive has enough free space and is mounted as writable.")
                sys.exit()
        try:
            suffix1 = generate_random_strings()
            suffix2 = generate_random_strings()
            suffix3 = generate_random_strings()
            suffix4 = generate_random_strings()
            p / f"Foldpro_test_folder_one{suffix1}".mkdir()
            p / f"Foldpro_Test_folder_two{suffix2}".mkdir()
            p / f"Foldpro_test_folder_three{suffix3}".mkdir()
            p / f"Foldpro_test_folder_four{suffix4}".mkdir()
        except Exception as e:
            if users_os == "macOS":
                errors.append("")
                
            elif users_os == "Windows":
            elif users_os == "Linux":






        
        
        



    
# TODO: Check if program can create folder in specific directory
# TODO: Verify move/create/delete permissions in copied folder
# TODO: Confirm ability to read specific folder name
# TODO: Test deletion of symlinks in copied version








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

    
