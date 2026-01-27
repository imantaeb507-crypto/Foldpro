# This module contains functions classes and variables that two or more other modules of the program will use

import re
from pathlib import Path

FILENAME_PATTERN = re.compile(r'^(?P<hidden>\.?)(?P<stem>.+?)(?P<suffix>(?:\.[^.]+)+)?$')


def isFold(path: Path) -> bool:
    '''
    Foldpros version of pathlibs path.is_dir() that doesnt follow symlinks.
    '''
    is_a_symlink = path.is_symlink()
    is_directory = path.is_dir()
    if is_a_symlink:
        return False
    return is_directory

def exists(p: Path) -> bool:
    '''
    Foldpros version of pathlibs path.exists() that doesnt follow symlinks.
    '''
    if p.is_symlink():
        return True
    return p.exists()


def getUniquePathComponents(p: Path) -> tuple[str, str, Path]:
    '''
    Helper for prettyUniquePath to get the stem, suffix and parent of a path while dealing with multi, sindgle suffix files, hidden files and any mixture of those.'''
    match = FILENAME_PATTERN.match(p.name)
    # The not p.is_symlink() is added here so that we dont classify symlinks whos targets are files into the symlink category
    if ((not p.is_symlink() ) and p.is_file()) and match:
        stem = match.group('hidden') + match.group('stem')
        suffix = match.group('suffix') if match.group('suffix') else ''
        parent = p.parent
    else:
        stem, suffix, parent = p.stem, p.suffix, p.parent
    return stem, suffix, parent




def prettyUniquePath(p: Path) -> Path:
    '''
    Helper used whenever we wanna get a unique path with minimal number appending.
    '''
    stem, suffix, parent = getUniquePathComponents(p)
    i = 0
    candidate = p
    while exists(candidate):
        candidate = parent / f"{stem}{i}{suffix}"
        i += 1
    return candidate

# The following custom errors are used to help code in Foldpro to communciate clearly with code in @clean_exit()
# Example:
# preflight_operations() may raise atomicCopyError if it fails to copy everythign in user given folder atomiclly which tells clean_exit that it needs to clean up any workspace folders left behind from the failed copy attempt.



class atomicCopyError(Exception):
    '''
    Raised when preflight_operations fails to copy everything in user given folder atomiclly.
    '''
    def __init__(self, errorCause: Exception, userFolderCopy: Path):
        self.errorCause = errorCause
        self.userFolderCopy = userFolderCopy
        

class partiallyOrganizedError(Exception):
    '''
    Raised when Foldpro_command has organized at least one file/folder but runs into an unexpected error before finishing.
    '''
    def __init__(self, errorCause: Exception):
        self.errorCause = errorCause


class nonAtomicMoveError(Exception):
    '''
    Raised when Foldpro fails to move all files to final location(~/Foldpro Copies*).
    P.S. It's called “NonAtomic” because shutil.move does not guarantee atomicity; an error during execution can occur mid-operation, resulting in a partial move.
    '''
    def __init__(self, errorCause: Exception, dest: Path):
        self.errorCause = errorCause
        self.dest = dest


class wrongOSError(Exception):
    '''
    Raised when the user is not running Foldpro on macOS.
    '''
    pass
class inValidInputError(Exception):
    '''
    Raised when the user gives an invalid input
    '''
    def __init__(self, errorMessage):
        self.errorMessage = errorMessage


class noPathGivenError(Exception):
    '''Raised when the user gives no path.'''
    pass
