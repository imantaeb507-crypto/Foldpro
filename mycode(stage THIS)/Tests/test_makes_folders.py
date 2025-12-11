# test_makes_folders.py
import pytest
from pathlib import Path
import shutil
from major_functions import Helper_functions
TMP_WS = Path.home() / "Projects" / "tmp_test_workspace"

@pytest.fixture
def cleanup_tmp():
    # Ensure a clean workspace before each test
    if TMP_WS.exists():
        shutil.rmtree(TMP_WS)
    TMP_WS.mkdir(parents=True, exist_ok=True)
    yield
    # Cleanup after test
    if TMP_WS.exists():
        shutil.rmtree(TMP_WS)

def test_makes_folders_creates_all_folders(cleanup_tmp):
    folder_names = ["folderA", "folderB", "folderC"]

    created = Helper_functions.makes_folders(folder_names=folder_names, parent_path=TMP_WS)

    # Check that all returned paths exist
    for path in created:
        assert path.exists()
        assert path.is_dir()
