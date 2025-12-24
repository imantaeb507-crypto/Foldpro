from major_functions import organize, Helper_functions
import pytest
from pathlib import Path
import copy
import random
import shutil

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

subfolders = ['Photos', 'Code Files', 'Downloads From Terminal', 'Others']

@pytest.fixture
def mimick_folder_deterministiclly():
    
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

    def random_loc():
        while True:
            yield random.choice(possible_locations)


    # Make 25 files: 10 Picture files, 7 Code Files, 3 download from terminal files and 5 other files, all in random locations:
    random_location = random_loc()
    pic_files = [next(random_location) / f'pic_file{i+1}{random.choice(image_extensions)}' for i in range(10)]
    c_files = [next(random_location) / f'c_file{i+1}{random.choice(code_extensions)}' for i in range(7)]
    d_terminal = [next(random_location) / f'd_terminal{i+1}{random.choice(TERMINAL_EXTENSIONS)}' for i in range(3)]
    other = [next(random_location) / f'an_other_file{i+1}' for i in range(5)]
    all = pic_files + c_files + d_terminal + other
    for path in all:
        path.touch()

    # make and return all 4 subfolders:
    created_subfolders = []
    for folder in subfolders:
        a_subfolder = (mock_workspace / folder)
        created_subfolders.append(a_subfolder)
        a_subfolder.mkdir()
    
    yield created_subfolders
    shutil.rmtree(mock_workspace)
    

    
@pytest.mark.parametrize("mode, expected_value", [('e', 25), ('p_only', 10), ('c_only', 7), ('d_only', 3), ('o_only', 5)])
def test_organize(mimick_folder_deterministiclly, mode, expected_value):
    PICTURES, CODE_FILES, DOWNLOADS_FROM_TERMINAL, OTHERS = mimick_folder_deterministiclly
    symlinks, files = Helper_functions.categorize_files_and_symlinks(PICTURES.parent)
    organize(files=files, symlinks=symlinks, mode=mode, PICTURES=PICTURES, CODE_FILES=CODE_FILES,DOWNLOADS_FROM_TERMINAL=DOWNLOADS_FROM_TERMINAL, OTHERS=OTHERS)

    # Count total amount of files in organized folders(in aggregate):
    total_organized = 0
    for folder in mimick_folder_deterministiclly:
        for _ in folder.rglob('*'):
            total_organized += 1
    assert total_organized == expected_value






