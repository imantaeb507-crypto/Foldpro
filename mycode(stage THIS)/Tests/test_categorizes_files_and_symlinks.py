# test_categorize_files_and_symlinks.py
import pytest
from pathlib import Path
import shutil
from major_functions import Helper_functions # replace with actual module

TMP_WS = Path.home() / "Projects" / "tmp_test_workspace"

@pytest.fixture
def setup_workspace():
    # Ensure a clean workspace
    if TMP_WS.exists():
        shutil.rmtree(TMP_WS)
    TMP_WS.mkdir(parents=True, exist_ok=True)

    # Create regular files
    file1 = TMP_WS / "file1.txt"
    file2 = TMP_WS / "file2.txt"
    file1.touch()
    file2.touch()

    # Create symlinks
    symlink1 = TMP_WS / "symlink1"
    symlink2 = TMP_WS / "symlink2"
    symlink1.symlink_to(file1)
    symlink2.symlink_to(file2)

    # Create a subdirectory (should be ignored)
    subfolder = TMP_WS / "subfolder"
    subfolder.mkdir()
    (subfolder / "nested_file.txt").touch()  # also a regular file inside subdir

    yield TMP_WS

    # Cleanup
    if TMP_WS.exists():
        shutil.rmtree(TMP_WS)

def test_categorize_files_and_symlinks(setup_workspace):
    symlinks, regular_files = Helper_functions.categorize_files_and_symlinks(setup_workspace)

    # Convert to sets of names for easier checking
    symlink_names = {p.name for p in symlinks}
    regular_names = {p.name for p in regular_files}

    # Check symlinks
    assert symlink_names == {"symlink1", "symlink2"}

    # Check regular files
    assert regular_names == {"file1.txt", "file2.txt", "nested_file.txt"}
