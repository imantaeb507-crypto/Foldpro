#!/Users/parvinnourian/Foldpro/.venv/bin/python
from pathlib import Path
import os
import sys
import re
from typing import Union, Optional, List
import platform
from Foundation import NSURL



def _exit():
    print('''
----------------------------------
Thank you for considering FoldPro.
----------------------------------
    ''')
    sys.exit()

def is_dir_and_exists() -> Path:
    # Converts the str given by the user to a form that the rest of the module can work with reliably(a normalized version, if you will):
    def _converts_to_canonical_version(p: str) -> Path:
        def _resolve_finder_display_names(path: Path) -> Path:
            """
            Input: Path object or string representing a path (can contain symlinks).
            Output: Path object pointing to the canonical filesystem path with all display names resolved.

            Works ONLY on macOS
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

    # Wrote the os_check so that Foldpro not working cant be blamed on me if someone who isnt using macOS runs it.
    def _os_check() -> None:
        if platform.system() != "Darwin":
            print("Sorry! Foldpro only works on the macOS operating system.")
            _exit()
    def pre_is_dir_and_exists_check(path: Path):
        def _traverse_error_checker(p: Path):
            """
            WHY: Ensures that every ancestor in the given path is traversable (has execute permission),
    starting from root, to prevent access or synchronization errors later in the program.
            INPUT: Path object (p)
            OUTPUT: True if all dirs are traversable; (False, Path(non_traversable_dir)) if one fails;
            False if a directory in the chain does not exist.
            """

            try:
                exists = True
                # Convert to absolute path to ensure full traversal from root
                p = p.resolve(strict=False)
                for ancestor in p.parents[::-1]:  # Start from root and go downward
                    if not ancestor.exists():
                        exists = False
                        return False  # Folder doesn’t exist at some level
                    if not os.access(ancestor, os.X_OK):  # Check execute permission
                        return (False, ancestor)
                if not os.access(p, os.X_OK):
                    return (False, p)
                return True

            except FileNotFoundError:
                exists = False
                return False
        # run function once for effiecency and store value for later use:
        _ = _traverse_error_checker(path)
        if _ == False:
            return f'''
The given path: '{path!s}' does not exist.\nPlease input a valid path or type 'e' to exit.
            '''
        elif isinstance(_, tuple):
            return f'''
Folder {_[1].name!s} is not transversable. In order to fix this, please follow the following steps and then re-run the program:

1.Run the following command in your terminal to make sure access isnt the issue(and to fix it if it is):
chmod u+x {_!s}
2.Run the following command and IF you see a user-name thats diffirent than your's run the second command.
Be warned, having to run this command means your trying to gain a Foldpro organized version of another users folder and is therefore NOT advised:
ls -ld {_!s}
# The 'groupname' is the name you'll find after the username when you run ls -ld {_!s}:
sudo dseditgroup -o edit -a YOUR_USERNAME -t user groupname
3.Navigate to the following:
System Settings --> Privacy & Security --> Full Disk Access
and toggle terminal to have full disk access

 '''


    print('''
********************************************************************************************************************        
Thank you for choosing FoldPro! Before we begin, FoldPro needs to check whether it can do certain things on your computer.
Throughout these series of checks, FoldPro might notify you about some problems it detects with either your file-permmisions and/or the path you gave it
Don't worry — all this means is that you have to take some quick actions(outlined in the error message) and/or enter a new path.
    
Start the check (y/n)?
    ''')
    _os_check()
    yes_and_its_equivalents = ['yes', 'yep', 'yup', 'y', 'yrp', 'mhmm']
    no_and_its_equivalents = ['no', 'n', 'nope', 'nah', 'nahh']
    exit_and_its_equivalents = ['e', 'exit', 'exitt']

    def prompt_for_path() -> Path:
        print("What is the path (absolute or relative) to the folder that you want to organize?")
        while True:
            raw = input('>')
            if raw in exit_and_its_equivalents:
                _exit()
            raw = _converts_to_canonical_version(raw)
            p = raw
            if not p.exists():
                print(f"The given path: '{p}' does not exist.\nPlease input a valid path or type 'e' to exit.")
                continue
            if not p.is_dir():
                print(f"'{p.name}' is not a folder. Please provide a valid folder path or type 'e' to exit.")
                continue
            return p

    while True:
        choice = input('>').strip().lower()

        if choice in yes_and_its_equivalents:
            return prompt_for_path()
        elif choice in no_and_its_equivalents:
            elaboration1 = input('''
What would you like to do, then:
- Begin Check (B)
- Exit Program (E)
> ''').strip().lower()
            if elaboration1 in exit_and_its_equivalents:
                _exit()
            elif elaboration1 in ['b', 'begin', 'begin check']:
                return prompt_for_path()
            else:
                print("Input not understood. Please reply with either 'b' for begin check or 'e' for exit.")
        elif choice in exit_and_its_equivalents:
            _exit()
        else:
            print("Input not understood. Please reply with either 'y' or 'n'.\n>")

is_dir_and_exists()

#TODO:Before you manipulate the contents of the folder move it under a unique folder name under tmp
#TODO:integrate the new helper function you just wrote
#TODO:write and integrate the stat function
#TODO: Check wether path exists and give an option too enter again if it dosent
#TODO: Same thing as the one above but just for wether its a dir or not
#For all of the below operations you need to give the option to change the file permissions right then and there:
#TODO: Check wether the folder can be copied like you need it to be copied
#TODO: delete all symlinks in the copied version
#TODO: Check wether the 4 folders can be created in the copied folder
#TODO: Move all files to random locations in the newly created folders
#TODO: make one dir in the copied version and try to delete it



def verifies_access():
     pass
