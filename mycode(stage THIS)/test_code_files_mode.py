import shutil
import random
import tempfile
from pathlib import Path
import pytest

from major_functions import file_organizer, Helper_functions

@pytest.mark.parametrize("runs", [5])
def test_file_organizer_c_only_deterministic(runs):
    """
    Deterministically exercise file_organizer() in 'c_only' mode.
    Runs the same scenario `runs` times, prints classification/moves for each run,
    and cleans up the workspace after all runs complete.
    """
    base = Path(tempfile.gettempdir()) / "foldpro_test_workspace"
    # ensure a clean base for this test run series
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True, exist_ok=True)

    # files to create each run (mixed types)
    sample_names = [
        "main.py", "helper.PY", "script.sh", "index.js", "module.ts",
        "image.svg", "photo.JPG", "readme.md", "archive.tar.gz", "notes.txt"
    ]

    for run in range(runs):
        random.seed(run)  # deterministic placement per-run
        run_dir = base / f"run_{run}"
        run_dir.mkdir(parents=True, exist_ok=True)

        # create organizer target folders
        PICTURES = run_dir / "Photos"
        CODE_FILES = run_dir / "Code Files"
        DOWNLOADS_FROM_TERMINAL = run_dir / "Downloads From Terminal"
        OTHERS = run_dir / "Others"
        for d in (PICTURES, CODE_FILES, DOWNLOADS_FROM_TERMINAL, OTHERS):
            d.mkdir(parents=True, exist_ok=True)

        # create files (place them directly under run_dir for clarity)
        files = []
        for name in sample_names:
            p = run_dir / name
            p.touch()
            files.append(p)

        # show initial classification by helper before organizing
        print(f"\n=== Run {run} initial classifications ===")
        for p in files:
            suffix = p.suffix.lower()
            is_code = suffix in {e.lower() for e in getattr(__import__("major_functions"), "code_extensions", [])}
            is_download = Helper_functions.is_download_from_terminal(p)
            print(f"{p.name:20} suffix={suffix:8} is_code={is_code:5} is_download={is_download}")

        # call the unit under test in 'c_only' mode
        file_organizer(files=files, subfolders=[PICTURES, CODE_FILES, DOWNLOADS_FROM_TERMINAL, OTHERS], mode="c_only")

        # report where each file ended up after organizing
        print(f"\n--- Run {run} results (where each file is) ---")
        for name in sample_names:
            src = run_dir / name
            loc = "MISSING"
            if (CODE_FILES / name).exists():
                loc = "CODE_FILES"
            elif (PICTURES / name).exists():
                loc = "PICTURES"
            elif (DOWNLOADS_FROM_TERMINAL / name).exists():
                loc = "DOWNLOADS"
            elif (OTHERS / name).exists():
                loc = "OTHERS"
            print(f"{name:20} -> {loc}")

    # cleanup after all runs
    print("\nCleaning up test workspace:", base)
    shutil.rmtree(base)






