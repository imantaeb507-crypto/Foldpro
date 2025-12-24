from pathlib import Path
import re
from typing import Tuple, Union, Optional
from FoldproHelpers import Formatter, YES, NO, EXIT, mk_random, unique_path
import sys
from rich.traceback import install
from rich import print
import os
import time
import shutil

install()
setup_formatter = Formatter(header="Setup", header_color="yellow")

# Makes workspace Folder and introduces program if this is the first time the users used Foldpro: 
def set_up_workspace() -> Tuple[Path, bool]:
   '''
   Makes Foldpro's workspace(if it dosent exist yet). This is where temporary folder copies will go to get organized.
   '''

   # This function figure out wether this is the first time a Foldpro command is running on a Users computer as part of its main task.
   # To make this information available for setup_instructions_wrapper(), 
   # I store it in this variable and return it as the last value so the other function can behave correctly.
   has_already_ran = False
   def _make_workspace() -> Tuple[Path, bool]:
       workspace = Path('/tmp/Foldpro-Workspace')
       workspace = unique_path(workspace)
       workspace.mkdir(parents=True)   #: Have Foldpro make the /tmp folder in case it dosent exist

       return workspace, has_already_ran


   # Find the already existing workspace(if there is one):
   pattern = re.compile(r"^Foldpro-Workspace(\d+)?$")
   matches = [Path(p) for p in Path("/tmp").iterdir() if p.is_dir() and pattern.match(p.name)]




   # If there already is a workspace, return it's path as a path object:
   if matches:
       has_already_ran = True
       workspace = matches[0]
       return workspace, has_already_ran
  
   # If not, make it, and then return it's path object:
   else:
       return (_make_workspace())
  

def set_up_instructions():
   '''
   Guides user through setup proccess
   '''


   print(setup_formatter.format(
   "1. Go to: System Settings --> Privacy & Security --> Full Disk Access\n"
   "\n"
   "2. Turn the botton for terminal on: [⚪────] --> [────🟢]\n"
   "\n"
   "3. IF you would like to organize a folder stored in iCloud store it in your drive by following the instructions in the following video:\n\n"
    "https://www.youtube.com/watch?v=wfX4rfVHY7s"

   "Type 'd' to move on."
   ))


   while True:
       feedback = input('>').strip().lower()
       if feedback in EXIT:
           sys.exit()
       if feedback in {'d', 'done'}:
           return
       else:
           print(setup_formatter.format(
           "Input not understood. Reply 'd' for done or 'e' to exit."
           ))


def setup_instructions_wrapper() -> None:
   '''
   Introduces user to Foldpro and walks them through setup proccess
   '''
  
   print('\n')
   print(setup_formatter.format(
   "Thanks for choosing FoldPro! Before we begin, we just need to perform a little setup.\n"
   "Please be warned that if these setup instructions aren't followed Foldpro might act unpredictably.\n"
   "Enter 'e' at any time to exit.\n\n"
   "Begin Setup? (y/n)"
   ))


   while True:
       choice = input('>').strip().lower()
       if choice in EXIT:
           sys.exit()


       if choice in YES:
           return set_up_instructions()


       elif choice in NO:
           print(setup_formatter.format(
           "What would you like to do, then:\n"
           "- Begin setup (S)\n"
           "- Exit Program (E)"
           ))
           while True:
               sub_choice = input('>').strip().lower()
               if sub_choice in EXIT:
                   sys.exit()
               elif sub_choice in {'s', 'setup', 'begin setup'}:
                   return set_up_instructions()
               else:
                   print(setup_formatter.format(
                   "Input not understood. Reply 'b' for begin setup or 'e' to exit."
                   ))


       elif choice in EXIT:
           sys.exit()


       else:
           print(setup_formatter.format(
           "Input not understood. Reply 'y' for begin setup or 'e' to exit."
           ))



def setup():
    workspace, has_already_ran = set_up_workspace()
    if not has_already_ran:
        setup_instructions_wrapper()
    return workspace




def canonical_version(path: str, header: Formatter) -> Union[Path, str]:
    """
    Converts a user-given path to a canonical absolute Path object that Foldpro can use.
    Handles symlinks, expands user shortcuts, and removes invisible characters.
    """

    path = Path(path)

    # Remove invisible characters and expand user (~)
    path = Path(re.sub(r'[\u200b\u00a0]', '', str(path))).expanduser()

    # Resolve symlinks if they exist
    if path.is_symlink():
        try:
            target = Path(os.readlink(path))  # Read symlink target
        except PermissionError:
            return header.format(
                "Foldpro doesn't have permission to access {}'s target. "
                "Please provide another path or grant Foldpro access and try again.".format(str(path))
            )

        # If the target is relative, resolve it relative to the symlink's parent
        if not target.is_absolute():
            target = path.parent / target

    # Ensure path is under home directory. Assume relative path is relative to home directory:
    if not path.is_absolute():
        path = Path.home() / path

    return path


def confirm_size_check(path: Path, header: Formatter) -> Optional[str]:
    '''Makes sure user is ok with copying a folder over 1gb and acts like a helper to get_good_path_and_confirm'''
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
        print(header.format("{} is over 1GB in size. Are you sure you would like to make an organized copy of it?".format(path.name)))
        while True:
            answer = input('>').strip().lower()
            if answer in EXIT:
                sys.exit()
            if answer in YES:
                return
            elif answer in NO:
                return header.format("Enter another path, then.")
            print(header.format("Input not understood. Reply 'y' to confirm or 'n' to disconfirm."))
    return None




def get_good_path_and_confirm(header: Formatter) -> Path:
    """
    Prompt the user until they enter a valid folder path that FoldPro can operate on.
    Performs checks for existence, directory type, home directory scope, Library, iCloud, size, and long paths.
    """

    print(header.format("Enter the path to the folder you would like to organize:"))

    icloud_root = Path.home() / "Library" / "Mobile Documents" / "com~apple~CloudDocs"
    library_root = Path.home() / "Library"
    MAX_DISPLAY_LENGTH = 53

    while True:
        raw_path = input('>').strip()
        if raw_path.lower() in EXIT:
            sys.exit()

        # Convert to canonical absolute path
        path = canonical_version(raw_path, header)
        if isinstance(path, str):
            print(path)
            continue

        # Helper function to display long paths neatly
        def display_path(p: str) -> str:
            if len(p) > MAX_DISPLAY_LENGTH:
                return "{}...{}".format(p[:5], p[-5:])
            return p
        
        # Prevent operating on iCloud folders
        if icloud_root in path.parents or path == icloud_root:
            print(header.format(
                "FoldPro cannot operate on folders stored in iCloud. "
                "Please move '{}' locally or enter another path".format(display_path(str(path)))
            ))
            continue

        # Prevent operating on Library folder or subfolders
        if library_root in path.parents or path == library_root:
            print(header.format(
                "Foldpro cannot operate on folders stored under [green]~/Library.[green]\n"
                "Please enter another path:"
            ))
            continue

        # Check existence
        if not path.exists():
            print(header.format(
                "The path '{}' does not exist. Enter a valid path or 'e' to exit.".format(display_path(raw_path))
            ))
            continue

        # Ensure it's a directory
        if not path.is_dir():
            print(header.format(
                "The path '{}' is not a folder. Enter a folder path.".format(display_path(raw_path))
            ))
            continue

        # Confirm size if over 1GB
        size_check = confirm_size_check(path, header)
        if isinstance(size_check, str):
            print(size_check)
            continue

        break

    return path





# Makes copy in workspace:
def mk_copy(workspace: Path, user_given_folder_copy: Path) -> Path:
    dest = unique_path(workspace / user_given_folder_copy.name)
    shutil.copytree(user_given_folder_copy, dest)
    return dest



def get_path_and_copy(header: Formatter, workspace: Path) -> Path:
    '''
    Prompts user until they give a valid path, makes workspace if it dosent exist, copies user-given folder to workspace to organize
    and returns the path to that copy(workspace).
    '''
    user_given_folder_path = get_good_path_and_confirm(header)
    workspace = mk_copy(workspace, user_given_folder_path)
    return workspace


workspace = setup()
get_path_and_copy(setup_formatter, workspace)
