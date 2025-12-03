# This module structures folder organization into clear, high-level functions, with detailed actions handled by helper methods for readability and maintainability.
from pathlib import Path
import random
import shutil
from typing import List, Dict, Tuple
from collections import defaultdict
import os
import re
from Helpers import Exit
from rich.traceback import install
install()
fail = Exit.fail
exit = Exit.exit

image_extensions = {
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif",
    ".heic", ".heif", ".webp", ".cr2", ".nef", ".arw", ".dng", ".svg"
}

code_extensions = {
    ".py", ".pyw", ".ipynb",
    ".js", ".ts", ".jsx", ".tsx",
    ".java", ".class",
    ".c", ".cpp", ".cxx", ".h",
    ".cs",
    ".rb",
    ".php", ".php3", ".php4", ".php5",
    ".go",
    ".swift",
    ".kt", ".kts",
    ".scala",
    ".m", ".mm",
    ".rs",
    ".sh", ".bash", ".zsh", ".ksh",
    ".r",
    ".pl", ".pm",
    ".sql",
    ".xml", ".json", ".yaml", ".yml"
}



class Helper_functions():
    # Used by both symlink_organizer() and symlink_categorizer():

    @staticmethod
    def is_download_from_terminal(p: Path) -> bool:
        TERMINAL_EXTENSIONS = {".sh", ".bash", ".zsh", ".tar.gz", ".tgz", ".zip", ".deb", ".rpm", ".pkg", ".out", ".log", ".whl"}
        TERMINAL_NAME_PATTERNS = ["setup", "install", "package", "v", "release"]

        PACKAGE_MANAGER_PATHS = [
            Path("/usr/local/bin"),
            Path("/opt/homebrew/bin"),
            Path.home() / ".cargo" / "bin",
            Path.home() / ".npm",
            Path.home() / ".local" / "bin",
        ]

        HIDDEN_CONFIG_FOLDERS = [
            Path.home() / ".cache",
            Path.home() / ".pip",
            Path.home() / ".npm",
            Path.home() / ".cargo",
            Path.home() / ".config",
        ]

        # Normalize path if symlink or has ~
        if p.is_symlink():
            p = p.expanduser().resolve(strict=False)

        def is_in_known_dirs(target: Path) -> bool:
            for folder in PACKAGE_MANAGER_PATHS + HIDDEN_CONFIG_FOLDERS:
                if folder in target.parents:
                    return True
            return False

        def has_terminal_extension(target: Path) -> bool:
            return target.suffix.lower() in TERMINAL_EXTENSIONS or \
                any(str(target).lower().endswith(ext) for ext in [".tar.gz", ".tgz"])

        def matches_name_pattern(target: Path) -> bool:
            return any(pattern in target.name.lower() for pattern in TERMINAL_NAME_PATTERNS)

        return is_in_known_dirs(p) or has_terminal_extension(p) or matches_name_pattern(p)

# ------------------------------------------------------------------------

    # Used by this modules wrapper function(organizes_folders):

    @staticmethod
    def categorize_files_and_symlinks(workspace: Path) -> Tuple[List[Path], List[Path]]:
        """
        Walk through `workspace` and return:
        - symlinks
        - regular files

        Hard links are NOT detected separately.
        Directories are ignored.
        """

        symlinks = []
        regular_files = []

        for entry in workspace.rglob("*"):
            # Skip directories entirely
            if entry.is_dir():
                continue

            # Symlink
            if entry.is_symlink():
                symlinks.append(entry)
                continue

            # Regular file
            try:
                entry.stat()  # ensures it's a real file
                regular_files.append(entry)
            except FileNotFoundError:
                # Broken symlink or race condition — treat as symlink
                symlinks.append(entry)

        return symlinks, regular_files

    @staticmethod
    def name_collison_prevention(p: Path) -> Dict[str, List[Path]]:
        modified_names = {}
        # Get a organized dictionary of all double occurences(collisons):
        name_map = defaultdict(list)

        for root, dirs, files in os.walk(p):
            # Record folders
            for d in dirs:
                full_path = os.path.join(root, d)
                name_map[d].append(full_path)

            for f in files:
                full_path = os.path.join(root, f)
                name_map[f].append(full_path)

        collisions = {name: paths for name, paths in name_map.items() if len(paths) > 1}
        # append random number to all double occurness so as to prevent future name collisons(and store original + modified version for future cleanup)
        folder_number = 0
        for value in collisions.values():
            for path in value:
                folder_number += 1
                modified_name = path.parent / (path.stem + str(random.randint(0,9999999999)))
                modified_names["folder" + str(folder_number)] = [path, modified_name]
                path.rename(modified_name)

        return modified_names
    
    @staticmethod
    def move_entrys(*, folders_to_move: List[Path], target_location: Path) -> None:
        for folder in folders_to_move:
            try:
                dest = target_location / folder.name
                shutil.move(str(folder), str(dest))
            except Exception as e:
                fail(f"Failed to move '{folder}' to '{target_location}': {e}")
    
    @staticmethod
    def makes_folders(*, folder_names: List[str], parent_path: Path) -> List[Path]:
        # Create the folders Foldpro is going to be organinzing into, append 4-digits if and until no collison occurs, and return the folders paths:
        folders = folder_names
        created_paths = []

        for folder_name in folder_names:
            try:

                folder_path = parent_path / folder_name
                while folder_path.exists():
                    folder_path = parent_path / f"{folder_name}{random.randint(0,9999)!s}"
                folder_path.mkdir(parents=True)
                created_paths.append(folder_path)

            except PermissionError:
                print(f"Permission error while creating folder '{folder_path}'.")
            except OSError as e:
                print(f"OS error while creating folder '{folder_path}': {e}.")
            except Exception as e:
                print(f"Unexpected error while creating folder '{folder_path}': {e}.")

        return created_paths
    
# ------------------------------------------------------------------------



# Main functionality:


def symlink_organizer() -> None:
    



def symlink_organizer(symlinks: List[Path]) -> None:
    # Categorize symlinks in user's folder into those that are broken or non-existent(non_organizable)
    # and into those that aren't(organizable_symlinks):
    organizable_symlinks = []
    non_organizable = []

    for symlink in symlinks:
        target = symlink.expanduser().resolve(strict=False)
        if target.is_dir() or not target.exists():
            non_organizable.append(symlink)  
        else:
            organizable_symlinks.append(symlink)

    # Organize all non_organizable's into others and the rest into one of the created subfolders according to their targets location:
    for sym in non_organizable:
        shutil.move(str(sym), str(OTHERS))
    for sym in organizable_symlinks:
        suffix = sym.suffix.lower()

        if suffix in image_extensions:
            shutil.move(str(sym), str(PICTURES / sym.name))

        elif suffix in code_extensions:
            shutil.move(str(sym), str(CODE_FILES / sym.name))

        elif Helper_functions.is_download_from_terminal(sym):
            shutil.move(str(sym), str(DOWNLOADS_FROM_TERMINAL / sym.name))
        else:
            shutil.move(str(sym), str(OTHERS / sym.name))

    


def regular_files_organizer(files) -> None:
    # Organize all files into their created subfolders via their extension names: 
    for file in files:
        if Helper_functions.is_download_from_terminal(file):
            shutil.move(str(file), str(DOWNLOADS_FROM_TERMINAL / file.name))
            files.remove(file)

    for file in files:
        if file.suffix in code_extensions:
            shutil.move(str(file), str(CODE_FILES / file.name))
            files.remove(file)


    for file in files:
        if file.suffix in image_extensions:
            shutil.move(str(file), str(PICTURES / file.name))
            files.remove(file)

    for item in files:
        shutil.move(str(item), str(OTHERS / item.name))



# Makes all the last little touches to the program. To be specific, it reverts all filenames that had numbers appended to them reverted back into their orginal form, it deletes the tmp workspace of foldpro and it creates then moves the organized folder into its destination.
def finalize_state(cleanup_data: Dict[str, List[Path]], workspace: Path,) -> None:
    # Delete all empty folders except the newly created ones(e.g.'Pictures'). 
    # This is done because FoldPro’s goal is to reorganize a user’s folder into the four directories defined in main:
    dont_delete = {PICTURES.name, DOWNLOADS_FROM_TERMINAL.name, OTHERS.name, CODE_FILES.name}
    for folder in p.iterdir():  
        if folder.name not in dont_delete:
            folder.rmdir()

    # Revert each entree name back into its orginal form. Keep looping until a 4-digit appendment stops collison from occuring:
    for old_path, new_path in cleanup_data.values():
        while old_path.exists():
            new_path = new_path.parents / f"{new_path}{random.randint(0,9999)!s}"
            old_path.replace(new_path) # revert all file and folder names that were modified to their orginal names
    for child in p.iterdir():
        if child.name in {PICTURES.name, CODE_FILES.name, DOWNLOADS_FROM_TERMINAL.name, OTHERS.name}:
            cleaned_child_name = re.sub(r'(?<=[A-Za-z])\d+$', '', child.name)
            child.rename(cleaned_child_name)

        foldpro_copys_folder = Path.home() / "Foldpro-Copies"

    # Make the folder that Foldpro will be storing the organized copy into:
    while foldpro_copys_folder.exists():
        foldpro_copys_folder = Path.home() / f"Foldpro-Copies{random.randint(0,99)}"

    foldpro_copys_folder.mkdir()

    # safely move the organized folder into the newly created folder:

    dest =  foldpro_copys_folder / workspace.name
    while dest.exists():
        dest = dest.parents() / f"{dest.name}{random.randint(0,999)!s}"
    shutil.move(str(workspace), str(dest))
    # delete the now-empty workspace folder
    workspace.rmdir()




# Wraps it all togetor:
def organizes_folders(p: Path) -> str:
    global PICTURES, CODE_FILES, DOWNLOADS_FROM_TERMINAL, OTHERS
    global symlinks, files
    workspace = create_workspace_and_copy(p)
    cleanup_data = Helper_functions.name_collison_prevention(workspace)
    PICTURES, CODE_FILES, DOWNLOADS_FROM_TERMINAL, OTHERS = Helper_functions.makes_folders(folder_names = ['Pictures', 'Code Files', 'Downloads From Terminal', 'Others'], parent_path = workspace)
    symlinks, files = Helper_functions.categorize_files_and_symlinks(workspace)
    symlink_organizer(symlinks)
    regular_files_organizer(files)
    
    finalize_state(cleanup_data, workspace)
    return "Organization complete. Would you like to tidy another one? If so, just write 'ta' for tidy again.\nIf not, just type 'e' to exit."



#TODO: Get unit tests done
#TODO: Implement every module level note to self(contained in main) in all 3 modules of Foldpro(except for the stuff that tells you how to package Foldpro in brew)
#TODO: make it able to repeatedy organize folders
#TODO: Make chatgpt rewrite a version of your code that is near unbreakable with robust error handling. Make sure to specify that you want the error messages to be actually helpfuel and applicable for the user and give it the already checked for list so it dosent give any repetive/uneccary instructions in the error messages. And also rememebr to tell it to use the fail function.
#TODO: After your absolutely sure that your code works exactly like you want it to work, get chatGPT to write a more organized version of it!
