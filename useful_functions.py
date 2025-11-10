from pathlib import Path
from typing import List
import random

def creates_folders(folder_list: List[str], dest: Path) -> List[Path]:
    """
    Assumptions:
        - The program has permission to make folders
        - The destination exists
        - You want a random 5-digit number appended to the end of the folder name if it already exists
    Inputs: 
        - folder_list: A list of the NAMES of the folders you want the function to create
        - dest: Where you want all of the folders to be created (Path object)

    Outputs:
        - A list of all the Path objects of the folders created. The sequence of Path objects corresponds 
          to the sequence of folder names given in folder_list.
    """
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
