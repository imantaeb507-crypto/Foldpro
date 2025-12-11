import pytest
from pathlib import Path
import shutil
from FoldproHelpers import mk_random
from setup import set_up_workspace, setup 


@pytest.fixture
def cleanup_tmp():
    """Cleanup any leftover Foldpro workspaces before and after tests."""
    pattern = "Foldpro-Workspace*"
    tmp = Path("/tmp")
    matches = [p for p in tmp.iterdir() if p.is_dir() and p.name.startswith("Foldpro-Workspace")]
    for folder in matches:
        shutil.rmtree(folder)
    yield
    # Clean up after test
    matches = [p for p in tmp.iterdir() if p.is_dir() and p.name.startswith("Foldpro-Workspace")]
    for folder in matches:
        shutil.rmtree(folder)


def test_workspace_creation(cleanup_tmp):
    """Test that a new workspace is created if none exists."""
    workspace, has_already_ran = set_up_workspace()
    assert workspace.exists()
    assert has_already_ran is False

    # Run again to test detection of existing workspace
    workspace2, has_already_ran2 = set_up_workspace()
    assert workspace2.exists()
    assert has_already_ran2 is True
    assert workspace2 == workspace
