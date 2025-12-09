# This module contains functions that two or more other modules of the program will use
from typing import Union, Optional
import os
import sys
import random
from pathlib import Path
import re
import time
from rich import print


# ---------------------------
# Exit and Fail helpers
# ---------------------------
class Exit:
    @staticmethod
    def fail(msg: str, fix_command: str = None):
        print(
            "============= Error ==============\n"
            f"FOLDPRO ERROR: {msg}", 
            file=sys.stderr
        )
        if fix_command:
            print(f"Shortcut to fix & retry:\n{fix_command}")
        sys.exit(1)

    @staticmethod
    def exit():
        print(
        "[bold]==================================[/bold]\n"
        "[bold]Thank you for considering FoldPro.[/bold]\n"
        "[bold]==================================[/bold]"
        )
        sys.exit()


class Formatter:
    '''
    I wanted this program to display messages in a consistent way that adapted to the mode the user is in.
    To accomplish that, I wrote this class.
    '''
    def __init__(self, header):
        self.header = header

    def format(self, *lines):
        formatted_message = [f"[bold]{self.header}[/bold]\n"]
        for line in lines:
            formatted_message.append(f"[bold]{line}[/bold]\n")
        return ( "".join(formatted_message).rstrip())
    
    


# User options that Foldpro will use for memebership checks:
YES = {'yes', 'yep', 'yup', 'y', 'yrp', 'mhmm'}
NO = {'no', 'n', 'nope', 'nah', 'nahh'}
EXIT = {'e', 'exit', 'q', 'quit'}

'''
class Foldpro_preflight_manager():
    def __enter__():
'''

foldpro_exit = Exit.exit

# makes however many random digits you tell it too:
def mk_random(amount_of_digits: int) -> str:
    digits = []
    for i in range(amount_of_digits):
        digits.append(str(random.randint(0,9)))
    digits = ''.join(digits)
    return digits


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




                












'''
def _preflight_permission_check() -> None:

    home = os.path.expanduser("~")

    # TCC-protected folders
    tcc_folders = ["Library/Messages", "Library/Mail", "Library/Calendars", "Library/Containers", "Library/Photos"]
    for folder in tcc_folders:
        path = os.path.join(home, folder)
        if os.path.exists(path):
            test_file = os.path.join(path, ".foldpro_tcc_test")
            try:
                with open(test_file, "w") as f:
                    f.write("test")
                os.remove(test_file)
            except Exception:
                fail(
f"Cannot write to TCC folder '{folder}'. Grant Full Disk Access.",
fix_command="Open System Settings → Privacy & Security → Full Disk Access → enable Terminal"
                )

    # ACL / extended attribute check
    acl_test = os.path.join(home, ".foldpro_acl_test")
    try:
        with open(acl_test, "w") as f:
            f.write("test")
        os.listxattr(acl_test)
        os.remove(acl_test)
    except Exception:
        fail(
"Cannot access extended attributes. Check ACL/permissions in home folder.",
fix_command=f"chmod -R u+rwX '{home}' && Foldpro"
        )

    # Cross-volume linking
    cross_src = os.path.join(home, ".foldpro_cross_src")
    cross_dst = "/tmp/.foldpro_cross_dst"
    try:
        with open(cross_src, "w") as f:
            f.write("test")
        try:
            os.link(cross_src, cross_dst)
        except OSError as e:
            if e.errno != errno.EXDEV:
                fail(
f"Unexpected cross-volume link error: {e}",
fix_command=f"Ensure source and /tmp are on same volume then run: Foldpro"
                )
        finally:
            for f in [cross_src, cross_dst]:
                try:
                    os.remove(f)
                except Exception:
                    pass
    except Exception:
        fail(
    "Cross-volume test failed. Check volumes and permissions.",
    fix_command="Ensure volumes are writable and retry: Foldpro"
'''
