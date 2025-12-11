from typing import Union, Optional
from FoldproHelpers import Formatter, foldpro_exit, YES, NO, EXIT
from pathlib import Path
import os
import re
import time


def canonical_version(path: str, header: Formatter) -> Union[Path, str]:
    '''
    Converts User-Given path to a form the rest of the program can work with more easily.
    Asks user to give the absolute version of the path if the one originally given is a symlink containing a relative path.
    It does this because symlinks can(and oftentimes are) stored in a diffirent location then the cwd.
    '''
    is_sym = False
    path = Path(path)

    # Resolve symlinks
    if path.is_symlink():
        is_sym = True
        path = Path(os.readlink(str(path)))

    # Remove invisible characters
    path = Path(re.sub(r'[\u200b\u00a0]', '', str(path)))
    path = path.expanduser()

    if not path.is_absolute() and is_sym:
        return (header.format(
                "Foldpro can't reliably work with symlinks containing relative paths. To fix this issue do [purple]one[/purple] of the following:",
                "- Enter absolute path of symlink's target",
                "- Enter another path (relative or absolute)",
                "",
                "New Path:"
                ))
    path = Path.home() / path
    return path

def confirm_size_check(path: Path, header: Formatter) -> Optional[str]:
    '''Makes sure user is ok with copying a folder over 1gb and acts like a helper to prompt_till_good_path'''
    def folder_size_in_gb(path: Path, timeout: float = 10.0) -> float:
        start_time = time.time()
        total_size = 0

        for root, dirs, files in os.walk(path):
            for file in files:
                try:
                    file_path = Path(root) / file
                    total_size += file_path.stat().st_size
                except (FileNotFoundError, PermissionError):
                    pass  # skip files we can't access
            
            # Check elapsed time
            if time.time() - start_time > timeout:
                # Return the current size in GB if timeout exceeded
                return total_size / 1024**3

        # Completed normally, return full size in GB
        return total_size / 1024**3
    
    # Calculate size:
    size_in_gb = folder_size_in_gb(path)

    # confirm if size is over 1GB. Return None(or a string) if not:
    if size_in_gb > 1:
        print(header.format(f"[green]{path.name}[/green] is over 1GB in size. Are you sure you would like to make an organized copy of it?"))
        while True:
            answer = input('>').strip().lower()
            if answer in YES:
                return
            elif answer in NO:
                return (header.format("Enter another path, then."))
            elif answer in EXIT:
                foldpro_exit()
            print(header.format("Input not understood. Reply 'y' to confirm or 'n' to disconfirm."))
    return None


def prompt_till_good_path(header: Formatter) -> Path:
    '''Prompt's user until they enter a valid path'''

    print(header.format(
    "Enter the path to the folder you would like to organize."
    ))
    while True:
        raw_path = input('>').strip()
        if raw_path in EXIT:
            foldpro_exit()
        icloud_root_possible_roots = {str(Path.home() / "library/icloud drive"), "~/library/icloud drive"}
        if raw_path.lower() in icloud_root_possible_roots:
            if len(raw_path) > 53:
                print(header.format(
                "FoldPro cannot operate on folders stored in iCloud.\n"
                f"Either enter a path that dosen't lead to an iCloud-stored folder or store [green]{raw_path[:5]}...{raw_path[-5:]}[/green] locally\n."
                ))
                continue
            else:
                print(header.format(
                "FoldPro cannot operate on folders stored in iCloud.\n"
                f"Either enter a path that dosen't lead to an iCloud-stored folder or store [green]{raw_path}[/green] locally\n."
                ))
                continue
        path = canonical_version(raw_path, header)
        if isinstance(path, str):
            print(path)
            continue
        if "Libary" in raw_path:
            print(header.format("Did you mean 'Library'?"))
            continue
        if not path.exists():
            # If the given path exceeds the lengh of 53 characters, have it be abbreviated with a ... sighn so as to keep the re-prompt looking relatively short:
            if len(raw_path) > 53:
                print(header.format(
                f"The path '{raw_path[:5]}...{raw_path[-5:]}' does not exist. Enter a valid path or 'e' to exit."
                ))
                continue
            else:
                print(header.format(
                f"The path '{raw_path}' does not exist. Enter a valid path or 'e' to exit."
                ))
                continue
        if not path.is_dir():
            print(header.format(
            "Please enter a path that does not lead to a file."
            ))
            continue
        if not str(path).startswith(str(Path.home())):
            print(header.format(
            "FoldPro can only operate on folders inside your home directory."
            ))
            continue
        # Foldpro will NEVER operate on anything under Libary due to how critical it is for the functionality of the users computer:
        forbidden_folder = str(Path.home() / "Library")
        if forbidden_folder in str(path):
            print(header.format("The Library folder is [red]far too risky[/red] for Foldpro to operate on. Please enter another path."))
            continue
        # If confirm_size_check returns none, we dont need to do anything sinse the folder is under one gb(since we only confirm with the user if the folder is more than one gb).
        # But, if it returns a string, we display that string so they can re-enter another path and that path can go through all the checks neccary.
        # The behavoir I've described above is showcased here:
        _ = confirm_size_check(path, header)
        if isinstance(_, str):
            print(_)
            continue
        break
    
    return path





def get_good_path(header: Formatter):
    prompt_till_good_path(header)

