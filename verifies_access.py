import os
import sys
import re
from pathlib import Path
from typing import Union
from Foundation import NSURL  # macOS-specific import


yes_and_its_equivalents = ['yes', 'yep', 'yup', 'y', 'yrp', 'mhmm']
no_and_its_equivalents = ['no', 'n', 'nope', 'nah', 'nahh']
exit_and_its_equivalents = {'e', 'exit', 'q', 'quit'}

def _exit():
    print(
        "----------------------------------\n"
        "Thank you for considering FoldPro.\n"
        "----------------------------------"
    )

# Determines whether the user wants to start the program or exit:
def _wants_to_start() -> None:
    print(
        "*******************************************************************************************\n"
        "Thanks for choosing FoldPro! Before we start, we need to make sure FoldPro can run properly on your computer.\n"
        "You'll just need to run a few quick terminal commands and toggle some settings—this will prevent most errors.\n"
        "If an error does happen, don't worry! It just means a small fix is needed, then you're ready to go.\n"
        "\n"
        "Start check? (y/n)"
    )

    while True:
        choice = input('>').strip().lower()

        if choice in yes_and_its_equivalents:
            return None

        elif choice in no_and_its_equivalents:
            print(
                "What would you like to do, then:\n"
                "- Begin check (B)\n"
                "- Exit Program (E)\n"
                ">"
            )
            while True:
                elaboration1 = input().strip().lower()

                if elaboration1 in exit_and_its_equivalents:
                    _exit()
                elif elaboration1 in ['b', 'begin', 'begin check', 'check']:
                    return None
                else:
                    print("Input not understood. Please reply with either 'b' for begin check or 'e' for exit.")

        elif choice in exit_and_its_equivalents:
            _exit()

        else:
            print("Input not understood. Please reply with either 'y' or 'n'.\n>")


def _preliminary_actions() -> None:
    try:
        def _ran_on_sudo() -> bool:
            geteuid = getattr(os, "geteuid", None)
            try:
                is_root = callable(geteuid) and os.geteuid() == 0
            except Exception as e:
                print(f"Unexpected error when checking sudo privileges: {e}")
                print("To fix this, please try the following:")
                print("  - Ensure you're running Foldpro using 'sudo Foldpro'.")
                print("  - Confirm Terminal has Full Disk Access in System Settings:")
                print("      Go to System Settings --> Privacy & Security --> Full Disk Access and turn Terminal on.")
                print("  - Use a standard macOS terminal like Terminal.app or iTerm")
                sys.exit()
                return False  # Fail-safe

            if not is_root:
                return False

            for var in ("SUDO_UID", "SUDO_USER", "SUDO_COMMAND"):
                try:
                    if os.environ.get(var):
                        return True
                except Exception as e:
                    try:
                        username = Path('~').expanduser().name
                    except Exception as e:
                        print(f"Unexpected error while retrieving the current username: {e}")
                        print("This usually happens if your home directory cannot be resolved.")
                        print("Permanent fix: Make sure your home directory exists. Then, restart the program.")
                        sys.exit()

                    print(f"Error accessing environment variable '{var}': {e}")
                    print("This likely means the variable isn't set.")
                    print("Permanent fix:")
                    print("  1. Run ONE of the following commands(no spaces):")
                    print(f'     echo "export {var}=\\"export SUDO_USER={username!s}\\"" >> ~/.zshrc  # Run if you are using Zsh')
                    print(f'     echo "export {var}=\\"export SUDO_USER={username!s}\\"" >> ~/.bashrc  # Run if you are using Bash')
                    print("  2. Press Command + S to save the file, close and re-open your terminal,")
                    print("     and then run the following command:")
                    print("      sudo Foldpro")
                    sys.exit()
            return False

        if _ran_on_sudo():
            print('''
Foldpro requires Full Disk Access to run. 
To enable it:
  1. Open System Settings → Privacy & Security → Full Disk Access, and turn on Terminal.
  2. Open System Settings → Apple Id → iCloud → Desktop & Documents Folders and turn off syncing for those folders.
  3. Return here and type 'd' when done''')
            while True:
                try:
                    user_status = input('>').strip().lower()
                except Exception as e:
                    print(f"Error reading input. Please type message again.")
                    continue

                if user_status in ['d', 'done']:
                    return None
                elif user_status in exit_and_its_equivalents:
                    _exit()
                else:
                    print("Message not understood. Please reply with either a 'd' for done or an 'e' for exit.")
        else:
            print('''
Foldpro needs to be run using sudo in order to work. Please restart the program properly with the following command:
sudo Foldpro''')
            sys.exit()

    except Exception as e:
        print(f"Unexpected error during preliminary actions: {e}")
        print("Please double check the following:")
        print("  1. You have Full Disk Access for the terminal")
        print("  2. You're running Foldpro using sudo")
        print("  3. Your current working directory is under 'Users'. If it isn't, run the following:\ncd ~ && sudo Foldpro")
        sys.exit()


def _prompt_till_good_path() -> Path:
    try:
        def _converts_to_canonical_version(p: str) -> Path:
            def _resolve_finder_display_names(path: Path) -> Path:
                def _get_symlink_target(path: Path) -> Path:
                    try:
                        if path.is_symlink():
                            try:
                                target = Path(os.readlink(str(path)))
                                return target
                            except PermissionError:
                                print(f"Insufficient permissions to resolve symlink: {path}")
                                print("FoldPro cannot access the target of this symbolic link due to missing permissions.")
                                print("Permanent fix:")
                                print("  1. Ensure you have read and execute permissions on both the symlink and its target folder:")
                                print(f"     chmod +rx '{path}'")
                                print("  2. If the target folder is missing or moved, update the symlink accordingly:")
                                print(f"     ln -s /path/to/target '{path}'")
                                print("After applying these steps, close and re-open the terminal, then run:")
                                print("sudo FoldPro")
                                sys.exit()
                    except OSError as e:
                        print(f"Error checking symlink for {path}: {e}")
                        print("This usually means the folder is broken or inaccessible.")
                        print("Permanent fix:")
                        print("  1. Verify that the folder which the symlink points to actually exists")
                        print("  2. If the folder was moved, update the symlink accordingly:")
                        print(f"    ln -s /path/to/target '{path}'")
                        print("  3. Ensure you have read permissions on the symlink and its target folder.")
                        print("After applying these steps, close then re-open the terminal and run the following:")
                        print("sudo Foldpro")
                        sys.exit()

                    return path

                path = _get_symlink_target(path)

                # Replace NSURL call with macOS-safe POSIX path resolution for older Python versions
                try:
                    real_path_str = os.path.realpath(str(path))
                except Exception as e:
                    print(f"Error resolving actual path for {path}: {e}")
                    print("Try ensuring Full Disk Access is granted and rerun with sudo:")
                    print("sudo Foldpro")
                    sys.exit()

                return Path(real_path_str)

            # Remove zero-width spaces
            p = re.sub(r'[\u200b\u00a0]', '', p)
            p = Path(p).expanduser()

            # Resolve finder names & actual paths
            p = _resolve_finder_display_names(p)

            # Path resolution wrapped for macOS protection
            try:
                p = Path(os.path.abspath(str(p)))
            except PermissionError:
                print(f"Permission denied resolving path: {p}")
                print("This usually means Foldpro doesn't have the necessary permissions to access this folder or one of its parent directories.")
                print("Permanent fix:")
                print("  1. Ensure the folder is inside your home directory (~).")
                print("  2. Make sure you have execute (traverse) permissions on this folder and all its parent directories:")
                print(f"     chmod +x '{p}'")
                print("  3. Restart Foldpro using sudo:")
                print("     sudo Foldpro")
                sys.exit()
            except Exception as e:
                print(f"Unexpected problem resolving path: {e}")
                print("This means something went wrong while Foldpro was trying to resolve the folder path.")
                print("Most likely causes and permanent fixes:")
                print("  1. Ensure the folder exists.")
                print("  2. Make sure you have permission to access this folder and all parent directories:")
                print(f"  chmod +x {p}")
                print("  3. Confirm the folder is inside your home directory (~).")
                print("After checking these, restart Foldpro using:")
                print("     sudo Foldpro")
                sys.exit()

            return p

        def _can_traverse(path: Path) -> Union[bool, str]:
            try:
                for ancestor in reversed(path.parents):
                    if not ancestor.exists():
                        return False
                    try:
                        if not os.access(str(ancestor), os.X_OK):
                            return (
                                f"FoldPro cannot enter the folder {ancestor} due to missing execute permissions.\n"
                                f"To fix this, run:\n"
                                f"chmod +x {ancestor} && sudo Foldpro"
                            )
                    except Exception as e:
                        return (
                            f"FoldPro was unable to access {ancestor}. This usually means your system permissions are unusual.\n"
                            f"Try running the following command in Terminal to fix it:\n"
                            f"chmod +x {ancestor} && sudo Foldpro\n"
                            f"Error details: {e}"
                        )

                if not os.access(str(path), os.X_OK):
                    return (
                        f"FoldPro cannot access the target folder {path} because execute permission is missing.\n"
                        f"Fix this by running:\n"
                        f'chmod +x "{path}" && sudo Foldpro'
                    )
            except Exception as e:
                return (
                    f"An unexpected error occurred while traversing the path {path}.\n"
                    f"This might be caused by unusual permissions or a corrupt filesystem.\n"
                    f"Try checking:\n"
                    f"1. That the folder and its parent directories exist.\n"
                    f"2. That you have execute permissions on them.\n"
                    f"3. That the filesystem is healthy.\n"
                    f"Error details: {e}"
                )

            return True

        def _starts_with_home(path: Path) -> Union[bool, str]:
            try:
                if not str(path).startswith(str(Path.home())):
                    return (
                        "FoldPro can only operate on folders inside your home directory.\n"
                        "Please input a path that is under your home directory or enter 'e' to exit."
                    )
            except Exception as e:
                return (
                    f"FoldPro was unable to verify whether the path {path} is inside your home directory.\n"
                    f"This may be caused by unusual filesystem or permissions settings.\n"
                    f"Error details: {e}"
                )
            return True

        def exists_locally(path: Path) -> bool:
            try:
                icloud_root = (Path.home() / "Library" / "Mobile Documents" / "com~apple~CloudDocs").resolve()
                if icloud_root in path.parents or path == icloud_root:
                    return False
            except Exception as e:
                print(
                    f"FoldPro encountered an error checking if the folder {path} is stored in iCloud.\n"
                    f"Make sure the folder exists locally and that your filesystem is accessible.\n"
                    f"Error details: {e}"
                )
                sys.exit()
            return True

        # main logic
        print(
            "What is the path (absolute or relative) to the folder that you would like to organize?\n"
            "P.S. Foldpro needs this information in order to check whether the path you gave it is valid and that all your file permissions are set up correctly."
        )
        while True:
            raw = input('>').strip().lower()
            if raw in exit_and_its_equivalents:
                _exit()
            normalized_version = _converts_to_canonical_version(raw)
            _ = _can_traverse(normalized_version)
            if _ == False:
                print("The given path doesn't exist. Please enter one that does or enter 'e' to exit.")
                continue
            if not exists_locally(normalized_version):
                print(f'''
The given folder does not exist locally on your computer and Foldpro can only operate on folders that do exist locally.
In order to make it exist locally (and re-run the program) please run the following command:
mv "{normalized_version}" "$HOME" && sudo Foldpro''')
                sys.exit()
            if isinstance(_, str):
                print(_)
                sys.exit()
            if not normalized_version.is_dir():
                print(f"{normalized_version.name} isn't a folder (Foldpro can only operate on folders).\nPlease enter a path that does lead to a folder or enter 'e' to exit.")
                continue
            __ = _starts_with_home(normalized_version)
            if isinstance(__, str):
                print(__)
                continue
            return normalized_version
    except Exception as e:
        print(f"Unexpected error in path prompt logic: {e}")
        print("Most likely causes and solutions:")
        print("  1. Path has unusual file system permissions")
        print("  2. Folder is on an external or unmounted drive")
        print("  3. You modified security settings recently - restart the terminal and try again")
        sys.exit()






#TODO:Use subproccess to make a copy of the volume in which their user directory is in and then move that to temp to be modified
#TODO:Implement code that stops the program from running if the file system being used is not APFS
#TODO:Write a functiont that moves symlinks to their appropiate folder if the meta data can be read, and moves it into its proper folder if its a broken symlink or its a folder 



'''
Permissions / conditions I've checked for already:
- Whether FoldPro has sudo access
- Whether FoldPro has Full Disk Access (it does)
- Whether the given path exists
- Whether the given path is a directory
- Whether the given path is under the user's home directory (~/Users)
- Whether the given folder exists locally (not in iCloud)
- Whether the user has execute (traverse) permission on every ancestor of the path, including the folder itself
- Whether symbolic links in the path can be resolved (with appropriate permissions)
- Whether the path can be resolved to its canonical absolute path safely
- Whether unusual filesystem or permission errors occur during path resolution
'''


def verifies_access():
    _wants_to_start()
    _preliminary_actions()
    valid_path =_prompt_till_good_path()

