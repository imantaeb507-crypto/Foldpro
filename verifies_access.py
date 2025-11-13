#!/Users/parvinnourian/Foldpro/.venv/bin/python
from pathlib import Path
import os
import sys
import re
from typing import Union, Optional, List, Any
from Foundation import NSURL
import subprocess

yes_and_its_equivalents = ['yes', 'yep', 'yup', 'y', 'yrp', 'mhmm']
no_and_its_equivalents = ['no', 'n', 'nope', 'nah', 'nahh']
exit_and_its_equivalents = ['e', 'exit', 'exitt']

def _exit():
    print(
        "----------------------------------\n"
        "Thank you for considering FoldPro.\n"
        "----------------------------------"
    )
    sys.exit()
# had these run here and not in any of the other checkers because one they vastly reduce the chances of the other code finding an error and second because it wouldnt make sense to run them later since there just fundamental things that Foldpro needs to work.   

# Determines wether the user wants to start the program or exit:
def _wants_to_start() -> bool:
    print(
    "*******************************************************************************************\n"        
    "Thanks for choosing FoldPro! Before we start, we need to make sure FoldPro can run properly on your computer.\n"
    "You'll just need to run a few quick terminal commands—this will prevent most errors.\n"
    "If an error does happen, don't worry! It just means a small fix is needed, then you’re ready to go.\n"
    "\n"
    "Start check? (y/n)"
    )
    while True:
        choice = input('>').strip().lower()

        if choice in yes_and_its_equivalents:
             return True
        elif choice in no_and_its_equivalents:
            elaboration1 = input(
                            "What would you like to do, then:\n"
                                "- Begin check (B)\n"
                                "- Exit Program (E)\n"
                                ">"
                            ).strip().lower()
            if elaboration1 in exit_and_its_equivalents:
                return False
            elif elaboration1 in ['b', 'begin', 'begin check', 'check']:
                return True
            else:
                print("Input not understood. Please reply with either 'b' for begin check or 'e' for exit.")
        elif choice in exit_and_its_equivalents:
            return False
        else:
            print("Input not understood. Please reply with either 'y' or 'n'.\n>")

# returns the 'good' path if the path given by the user exists, is a directory and is under ~. It will return an error message regarding permmissions and exit when needed.
def _prompt_till_good_path():
    # Converts the path string given by the user to a form that the rest of the module can work with reliably(a normalized version, if you will):
    def _converts_to_canonical_version(p: str) -> Path:
        def _resolve_finder_display_names(path: Path) -> Path:
            """
            Input: Path object or string representing a path (can contain symlinks).
            Output: Path object pointing to the canonical filesystem path with all display names resolved.
            """

            # Convert Path to NSURL
            url = NSURL.fileURLWithPath_(str(path))

            # Get the real filesystem path from NSURL (resolves symlinks, display names)
            real_path_str = url.path()

            # Return as Path object
            return Path(real_path_str)
        p = re.sub(r'[\u200b\u00a0]', '', p)
        p = Path(p)
        p = p.expanduser()
        p = _resolve_finder_display_names(p)
        p = p.resolve(strict = False)
        return p
    
    def _can_traverse(path: Path) -> Union[bool, str]:
        # iterate ancestors from root down to immediate parent
        for ancestor in reversed(path.parents):
            if not ancestor.exists():
                return False
            if not os.access(str(ancestor), os.X_OK):
                err_msg =(
                f"In order for FoldPro to work, it needs execute permission on {ancestor}\n"
                f"To give it that (and restart the program), run:\n"
                f"chmod +x {path} && Foldpro"
                )
                return err_msg

        if path.exists() and not os.access(str(path), os.X_OK):
            err_msg =(
            f"In order for FoldPro to work, it needs execute permission on the target {path}\n"
            f"To give it that (and restart the program), run:\n"
            f'chmod +x "{path}" && Sudo Foldpro'
            )
            return err_msg

        return True
    def _starts_with_home(path: Path) -> bool:
        if not str(path).startswith(str(Path.home())):
            return f'''
Foldpro can only operate on folders in the Users directory.
Please give a path inside your home directory or enter 'e' to exit.'''
        return True
    

    # main logic
    print("What is the path(absolute or relative) to the folder that you would like too organize?\nP.S.Foldpro needs this information in order to check wether the paht you gave it is valid and that all your file permmmisions are set up correctly.")
    while True:
        raw = input('>')
        if raw in exit_and_its_equivalents:
            _exit()
        normalized_version = _converts_to_canonical_version(raw)
        _ = _can_traverse(normalized_version)
        if _ == False:
            print("The given path dosent exist. Please enter one that does or enter 'e' to exit.")
            continue
        if isinstance(_, str):
            print(_)
            sys.exit()
        if normalized_version.is_dir():
            print("f{raw.name!s} isnt a folder(Foldpro can only operate on folders).\nPlease enter a path that does lead to a folder or enter 'e' to exit.")
            continue
        __ = _starts_with_home(normalized_version)
        if isinstance(__, str):
            print(__)
            continue
        return normalized_version


# The following function guides the user through giving Foldpro Sudo and full disk accces and its called preliminary actions because its what will run before the nitty gritty file permmmision checks since if the user graduates from this function the rest of the program checks are far unlikely to prop up errors for the user 
def preliminary_actions() -> type[None]:

    def _ran_on_sudo() -> bool:
        """
        Checks if the program is running with sudo privileges.
        If not, prompts the user for their password to test sudo access.
        Exits the program if sudo is not granted.
        """
        if os.geteuid() == 0:
            # Already running as root
            return True

        # Try a harmless sudo command to prompt for password
        try:
            result = subprocess.run(
                ['sudo', '-v'],  # '-v' just validates credentials
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            if result.returncode == 0:
                return True  # Sudo password accepted
            else:
                raise subprocess.SubprocessError
        except Exception:
            print(
            "Please enter the password correctly or run Foldpro with sudo if you would like to continue. Command:\n"
            "Sudo Foldpro"
            )
            sys.exit()        
    _ran_on_sudo()
    def _toggle_disk_access() -> type[None]:
    user_input =input("""\
                In order for foldpro to work, it needs full disk access(if you dont do this step, Foldpro will most likely not work). To give it that, please follow the instructions below or type 'e' to exit.\n
                1.Go to System Settings -> Privacy & Security -> Full Disk Access and toggle Terminal 'On'.\n'
                2.Type 'd' to continue\n
                >""")


#TODO:Figure out if ACLS and RWX permmsions on folders and files is all you have too worry about
#TODO:Figure out how too write code to account for ACLS
#TODO:Use subproccess to make a copy of the volume in which their user directory is in and then move that to temp to be modified
#TODO:Implement code that stops the program from running if the file system being used is not APFS
#TODO:Write a functiont that moves symlinks to their appropiate folder if the meta data can be read, and moves it into its proper folder if its a broken symlink or its a folder 
#TODO:As part of the check, have the user modify some settings if there current settings have the stuff under ~ as being ICloud synced
#TODO: Check wether path exists and give an option too enter again if it dosent
#TODO: Same thing as the one above but just for wether its a dir or not
#For all the tasks below have the user run some sort of command to make sure that the program has access:
#TODO: Check wether the folder can be copied like you need it to be copied
#TODO: delete all symlinks in the copied version
#TODO: Check wether the 4 folders can be created in the copied folder
#TODO: Move all files to random locations in the newly created folders
#TODO: make one dir in the copied version and try to delete it



def verifies_access():
    if _wants_to_start() != True:
        _exit()
    valid_path =_prompt_till_good_path()

    

