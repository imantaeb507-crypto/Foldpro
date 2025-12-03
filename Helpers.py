# This module contains functions that two or more other modules of the program will use

import os
import sys
import random
from pathlib import Path
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
            "==================================\n"
            "Thank you for considering FoldPro.\n"
            "=================================="
        )
        sys.exit()


class Formatter:
    '''
    I wanted this program to display messages in a consistent way that adapted to the mode the user is in.
    And to accomplish that, I wrote this class.
    '''
    def __init__(self, header):
        self.header = header

    def format(self, *lines):
        formatted_message = [f"[bold]{self.header}[/bold]\n"]
        for line in lines:
            formatted_message.append(f"[bold]{line}[/bold]\n")
        return "".join(formatted_message).rstrip()
    
# User options that Foldpro will use for memebership checks:
YES = {'yes', 'yep', 'yup', 'y', 'yrp', 'mhmm'}
NO = {'no', 'n', 'nope', 'nah', 'nahh'}
EXIT = {'e', 'exit', 'q', 'quit'}

'''
class Foldpro_preflight_manager():
    def __enter__():
'''   


def mk_random(amount_of_digits: int) -> str:
    digits = []
    for i in range(amount_of_digits):
        digits.append(str(random.randint(0,9)))
    digits = ''.join(digits)
    return digits


def _resolve_path(user_input: str) -> Path:
    """
    Converts user path to canonical, absolute Path object,
    resolves symlinks safely, and removes zero-width spaces.
    """
    def _resolve_symlink(path: Path) -> Path:
        if path.is_symlink():
            target = Path(os.readlink(str(path)))
            return target
        return path
    

def _prompt_till_good_path() -> Path:
    print(
"==================================\n"
"Enter the path (absolute or relative) to the folder you want to organize:"
    )
    while True:
        raw_path = input('>').strip().lower()
        if raw_path in EXIT:
            exit()
        path = _resolve_path(raw_path)

        if not path.exists():
            print(
"==================================\n"
"The path does not exist. Enter a valid path or 'e' to exit."
            )
            continue
        if not path.is_dir():
            print(
"==================================\n"
"Please enter a path that does not lead to a file."
            )
            continue
        if not str(path).startswith(str(Path.home())):
            print(
"==================================\n"
"FoldPro can only operate on folders inside your home directory."
            )
            continue
        icloud_root = Path.home() / "Library/Mobile Documents/com~apple~CloudDocs"
        if icloud_root in path.parents:
            fail(
"FoldPro cannot operate on iCloud-only folders. Ensure folder exists locally.",
fix_command=f"mv '{path}' '$HOME' && Foldpro"
            )

        # Traverse check
        for ancestor in reversed(path.parents):
            if not os.access(str(ancestor), os.X_OK):
                fail(
f"Cannot enter folder {ancestor}. Missing execute permissions.",
fix_command=f"chmod +x '{ancestor}' && Foldpro"
                )
        if not os.access(str(path), os.X_OK):
            fail(
f"Cannot access folder {path}. Missing execute permissions.",
fix_command=f"chmod +x '{path}' && Foldpro"
            )

        return path

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


