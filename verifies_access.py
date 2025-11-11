#!/Users/parvinnourian/Foldpro/.venv/bin/python
from pathlib import Path
import os
import sys
import re
from typing import Union, Optional, List, Any
import platform
from Foundation import NSURL

yes_and_its_equivalents = ['yes', 'yep', 'yup', 'y', 'yrp', 'mhmm']
no_and_its_equivalents = ['no', 'n', 'nope', 'nah', 'nahh']
exit_and_its_equivalents = ['e', 'exit', 'exitt']


def _exit():
    print('''
----------------------------------
Thank you for considering FoldPro.
----------------------------------
    ''')
    sys.exit()
# Determines wether the user wants to start the program or exit:
def _wants_to_start() -> bool:
    print('''
*******************************************************************************************        
Thanks for choosing FoldPro! Before we start, we need to make sure FoldPro can run properly on your computer.

You'll just need to run a few quick terminal commands—this will prevent most errors.
If an error does happen, don't worry! It just means a small fix is needed, then you’re ready to go.

Start check? (y/n)
    ''')
    while True:
        choice = input('>').strip().lower()

        if choice in yes_and_its_equivalents:
             return True
        elif choice in no_and_its_equivalents:
            elaboration1 = input('''
What would you like to do, then:
- Begin check (B)
- Exit Program (E)
> ''').strip().lower()
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

# Makes sure that is_dir_and_exists will work properly:
def pre_is_dir_and_exists(p: Path) -> None:
    pass


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
def is_sensitive_directory(path: Path) -> Union[type[bool], str]:
    def is_in_users_application_folder(path: Path) -> bool:
        return path.as_posix().startswith(str(Path.home() / "Applications"))

    def _is_applications_path(path: Path) -> bool:
        return path.as_posix().startswith("/Applications")

    def _is_library_path(path: Path) -> bool:
        return path.as_posix().startswith("/Library")

    def _is_system_path(path: Path) -> bool:
        return path.as_posix().startswith("/System")
    
    def _is_in_users_library(path: Path) -> bool:
        return path.as_posix().startswith(str(Path.home() / "Library"))        

    # main logic
    if _is_system_path():
        return f'''
Foldpro cannot operate safely on {path.name!s} becuse it is in system domain.
Please give a path that is in the user domain or type 'e' to exit.
'''
    


#TODO:Get is_sensitive_directory() written:
'''
-Figure out what are ALL of the directorys that are too dangerous for Foldpro too touch:
    *Absolutely NO messing with ANYTHING in the system domain, local domain, or anything under ~/Libarys
Inputs/Outputs:
    *INPUTS:the path object object
    *True if it isnt a a sensitive directory. Returns an appropiate error message if it isnt
-Integration:
    *Keeps prompting until a valid path is given
'''














#TODO:Figure out how your going to get Foldpro to safely copy any safe directory under users to tmp and then move it back again without causing errors: this is one of THE MOST important things to get right so take your time
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
    if _wants_to_start() == True:
        #Where the rest of the the code will go
        pass
    else:
        _exit()

