from pathlib import Path
import re
from typing import Union, Optional
from .foldproHelpers import isFold, atomicCopyError, inValidInputError, prettyUniquePath
import os
import shutil


# Constants
ICLOUD_ROOT = Path.home() / "Library"
LIBRARY_ROOT = Path.home() / "Library"
MAX_DISPLAY_LENGTH = 83
SIZE_LIMIT_GB = 1.0



# ============================================================================
# WORKSPACE SETUP
# ============================================================================

def getWorkspace() -> Path:
    """
    Create or find Foldpro's workspace in /tmp.
    Returns workspace path.
    """
    # Check if workspace already exists
    pattern = re.compile(r"^\.Foldpro-Workspace(\d)*$")
    existing = next(
        (p for p in Path("/tmp").iterdir() if isFold(p) and pattern.match(p.name)),
        None
    )
    
    if existing:
        return existing
    
    # Create new workspace
    workspace = prettyUniquePath(p = Path('/tmp/.Foldpro-Workspace'))
    workspace.mkdir()
    return workspace

# ============================================================================
# PATH VALIDATION
# ============================================================================

def display_path(path_str: str) -> str:
    """Truncate long paths for display."""
    if len(path_str) > MAX_DISPLAY_LENGTH:
        return f"{path_str[:5]}...{path_str[-5:]}"
    return path_str


def canonical_version(path: str) -> Union[Path, str]:
    """
    Convert user path to canonical absolute Path.
    Returns Path on success, error string on failure.
    """
    path = Path(path)
    
    # Remove invisible characters and expand ~
    path = Path(re.sub(r'[\u200b\u00a0]', '', str(path))).expanduser()
    
    # Resolve symlinks
    if path.is_symlink():
        try:
            target = Path(os.readlink(path))
        except PermissionError:
            return (
                f"Foldpro doesn't have permission to access {path}'s target. "
                "Please provide another path or grant access and try again."
            )
        
        # Resolve relative targets
        if not target.is_absolute():
            target = path.parent / target
        return target
    
    # Convert relative paths to absolute
    if not path.is_absolute():
        path = Path.cwd() / path
    
    return path


def validate_path(path: Path) -> Optional[str]:
    """
    Validate path meets all requirements.
    Returns None if valid, error message string if invalid.
    """
    # Check existence
    if not path.exists():
        return f"The path '{display_path(str(path))}' does not exist."
    
    # Check if directory
    if not path.is_dir():
        return f"The entree '{display_path(str(path))}' is not a folder."
    
    # Check under home directory
    if Path.home() not in path.parents and path != Path.home():
        return (
            "FoldPro can only operate on folders within your home directory. "
            "Please enter a valid path."
        )
    
    # Check not in iCloud
    if ICLOUD_ROOT in path.parents or path == ICLOUD_ROOT:
        return (
            f"FoldPro cannot operate on folders stored in iCloud. "
            f"Please move '{display_path(str(path))}' locally or enter another path."
        )
    
    # Check not in Library
    if LIBRARY_ROOT in path.parents or path == LIBRARY_ROOT:
        return (
            "Foldpro cannot operate on folders under ~/Library. "
            "Please enter another path."
        )
    
    return None


def confirmPath(userFolder: Path) -> Path:
    # Convert to canonical path
    path = canonical_version(userFolder)
    if isinstance(path, str):  # Error occurred
        raise inValidInputError(errorMessage = path)

    # Validate path
    error = validate_path(path)
    if error:
        raise inValidInputError(errorMessage = error)
    return path


# ============================================================================
# FOLDER COPYING & WRAPPER
# ============================================================================

def mkCopy(workspace: Path, sourceFolder: Path) -> Path:
    """
    Copy source folder to workspace with unique name.
    Returns path to the copy.
    """
    dest = prettyUniquePath(p=workspace / sourceFolder.name )
    
    try:
        shutil.copytree(sourceFolder, dest, symlinks=True)
    except Exception as e:
        raise atomicCopyError(errorCause = e, userFolderCopy = sourceFolder)
    
    return dest


def preFlightOperations(userFolder: Path) -> Path:
    """
    Perform all preflight operations and make sure users OS is macOS.
    Returns path to user's folder copy in workspace.
    """
    workspace = getWorkspace()
    userFolder = confirmPath(userFolder)
    userFolderCopy = mkCopy(workspace=workspace, sourceFolder=userFolder)
    return userFolderCopy
