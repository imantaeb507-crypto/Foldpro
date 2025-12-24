from major_functions import Helper_functions
import pytest
from pathlib import Path
import shutil
from FoldproHelpers import mk_random
import random
import copy



def mock_workspace():
    '''
    Makes a folder which emulates a folder which the user could give to Foldpro.
    It has 5 subfolders directly under the mock_workspace and 25 files and folders randomly placed among those 5 subfolder.
    '''
    image_extensions = [
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif",
    ".heic", ".heif", ".webp", ".cr2", ".nef", ".arw", ".dng", ".svg"
    ]

    code_extensions = [
        ".py", ".pyw", ".ipynb",
        ".js", ".ts", ".jsx", ".tsx",
        ".java", ".class",
        ".c", ".cpp", ".cxx", ".h",
        ".cs",
        ".rb",
        ".php", ".php3", ".php4", ".php5",
        ".go",
        ".swift",
        ".kt", ".kts",
        ".scala",
        ".m", ".mm",
        ".rs",
        ".sh", ".bash", ".zsh", ".ksh",
        ".r",
        ".pl", ".pm",
        ".sql",
        ".xml", ".json", ".yaml", ".yml"
    ]

    TERMINAL_EXTENSIONS = [".sh", ".bash", ".zsh", ".tar.gz", ".tgz", ".zip", ".deb", ".rpm", ".pkg", ".out", ".log", ".whl"]

    all_possible_extensions = image_extensions + code_extensions + TERMINAL_EXTENSIONS
    mock_workspace = Path.home() / 'Projects' / 'mock_workspace'
    mock_workspace.mkdir()


    # 5 surface level subfolders:
    base_subfolders = [mock_workspace / f'base_subfolder{i+1}' for i in range(5)]
    for folder in base_subfolders:
        folder.mkdir()

    # Makes 25 subfolders in random locations under the mock_workspace:
    possible_locations = copy.deepcopy(base_subfolders)
    for i in range(25):
        base_dest = random.choice(possible_locations)
        dest =  base_dest / f"folder_number{i+1}"
        possible_locations.append(dest)
        dest.mkdir()

    # Make 25 sub-files in random locations under the subfolders in ~/Projects/mock_workspace:
    for i in range(25):
        base_dest = random.choice(possible_locations)
        dest =  base_dest / f"file_number{i+1}.{random.choice(all_possible_extensions)}"
        dest.touch()





def test_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            mock_workspace()
            func(*args, **kwargs)
        finally:
            shutil.rmtree(Path.home() / 'Projects' / 'mock_workspace')
    return wrapper



