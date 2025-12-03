from setup import set_up_workspace
import re
import shutil
from pathlib import Path


def test_1():
    workspace = None   # <-- IMPORTANT

    try:
        folder_copies, history_dir = set_up_workspace()

        # Convert to strings for regex matching
        folder_copies_str = str(folder_copies)
        history_dir_str = str(history_dir)

        copies_re = re.compile(r'^/tmp/Foldpro-Workspace\d{15}/tmp_folder_copies$')
        history_re = re.compile(r'^/tmp/Foldpro-Workspace\d{15}/history_dir$')

        assert copies_re.search(folder_copies_str) is not None
        assert history_re.search(history_dir_str) is not None

        workspace_re = re.compile(r'^Foldpro-Workspace\d{15}$')
        matches = [
            p for p in Path('/tmp').iterdir()
            if p.is_dir() and workspace_re.search(p.name)
        ]

        assert len(matches) >= 1

        workspace = matches[0]     
        assert (workspace / "tmp_folder_copies").exists()
        assert (workspace / "history_dir").exists()

    finally:
        if workspace and workspace.exists():   # <-- prevents crashes
            shutil.rmtree(workspace)



#make sure the code dosent do anything if the folder already exists:
def test_2():
    workspace = None  # Safety for cleanup

    try:
        # First call creates the workspace
        folder_copies_1, history_dir_1 = set_up_workspace()
        workspace_1 = folder_copies_1.parent

        # Second call should NOT create a new workspace
        folder_copies_2, history_dir_2 = set_up_workspace()
        workspace_2 = folder_copies_2.parent

        # They must be the same workspace
        assert workspace_1 == workspace_2

        # And their subfolders must match
        assert folder_copies_1 == folder_copies_2
        assert history_dir_1 == history_dir_2

        # Ensure no additional workspace folders were created
        workspace_re = re.compile(r'^Foldpro-Workspace\d{15}$')
        matches = [
            Path(p) for p in Path('/tmp').iterdir()
            if p.is_dir() and workspace_re.match(p.name)
        ]

        # There must be exactly ONE workspace after two calls
        assert len(matches) == 1

        workspace = workspace_1  # Save for cleanup

    finally:
        # Clean up the workspace folder safely
        if workspace and workspace.exists():
            shutil.rmtree(workspace)









