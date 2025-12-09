from Helpers import prompt_till_good_path, Formatter
from pathlib import Path
import shutil
import os
from setup import setup_formatter

def prompt_till_good_path_decorator(func):
    def wrapper(formatter_object: Formatter):
        # Temporary test area
        base = Path("/Users/parvinnourian/Projects/TestArea")
        target = base / "OriginalFolder"
        link = base / "LinkToFolder9090"

        # Always start from a clean state
        if base.exists():
            shutil.rmtree(base)

        # Recreate base + target directory
        target.mkdir(parents=True, exist_ok=True)

        # Compute relative path safely (string)
        relative_target = os.path.relpath(target, link.parent)

        # Ensure link parent exists (link.parent == base)
        link.parent.mkdir(parents=True, exist_ok=True)

        # Create the symlink — guaranteed not to already exist
        link.symlink_to(relative_target)

        try:
            func(formatter_object)
        finally:
            # Clean the test area
            shutil.rmtree(base, ignore_errors=True)

    return wrapper


@prompt_till_good_path_decorator
def test_prompt(formatter: Formatter):
    prompt_till_good_path(formatter)


# Run the wrapped function
test_prompt(setup_formatter)
