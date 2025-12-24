from major_functions import Helper_functions
import pytest
from pathlib import Path
import shutil
from FoldproHelpers import mk_random
import random


# Set up mock workspace and its structure(5 folders on the first level, 5 in each, all nested one level more than its predeccesor).
# Also, cleanup once test is done with

@pytest.fixture
def mock_workspace():
    mock_workspace = Path.home() / 'Projects' / 'mock_workspace'
    mock_workspace.mkdir()


    # 5 surface level subfolders:
    surface_level_subfolders = [mock_workspace / f'sl_folder{i+1}' for i in range(5)]
    for folder in surface_level_subfolders:
        folder.mkdir()

    # The five subfolders, all nested below the other, under every surface level subfolder
    all_subfolders_made = [] # this variable is useful later on when we want to choose a random location to place a file in
    for i in range(5):
        folders_to_be_made = [mock_workspace / f"sl_folder{i+1}" / f"a_subfolder{j+1}" for j in range(5)]

        all_subfolders_made.append(folders_to_be_made)
        for folder in folders_to_be_made:
            folder.mkdir()

    # Flatten all_subfolders_made:
    all_subfolders_made = [path_object for sub_list in all_subfolders_made for path_object in sub_list]
    

    # Make the path for 10 ranodm files and 10 random symlinks under anywhere in the workspace. We append 5 random numbers to the end of their names so as to prevent collisons.
    # We also store the location of all the files so we can later use it as a target for the symlinks:
    possible_locations = surface_level_subfolders + all_subfolders_made
    file_destinations = []
    for i in range(10):
        dest = random.choice(possible_locations)
        name = f"a_file{mk_random(5)}"
        file_dest = dest / name
        file_destinations.append(file_dest)
        file_dest.touch()
    for target in file_destinations:
        dest = random.choice(possible_locations)
        name = f"a_symlink{mk_random(5)}"
        symlink_location = dest / name
        symlink_location.symlink_to(target)

    yield mock_workspace
    shutil.rmtree(mock_workspace)



def test_categorizes_files_and_symlinks(mock_workspace):
    symlinks, files = Helper_functions.categorize_files_and_symlinks(mock_workspace)
    assert isinstance(symlinks, list)
    assert isinstance(files, list)
    assert len(symlinks) == 10
    assert len(files) == 10
    