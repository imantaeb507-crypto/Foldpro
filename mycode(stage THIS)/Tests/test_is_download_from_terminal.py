from major_functions import Helper_functions
from typing import List
from pathlib import Path
import shutil
import pytest

# make referencing the helper function less tedious:
is_download_from_terminal = Helper_functions.is_download_from_terminal

def cleanup(created: List[Path]):
    for entree in created:
        if entree.exists():
            if entree.is_dir():
                shutil.rmtree(str(entree))
            else:
                entree.unlink()

tmp_ws = Path(Path.home() / 'Projects/tmp_ws')
should_return_true_too = tmp_ws / "trues"
should_return_false_too = tmp_ws / "falses"

# Create folder to test on:

@pytest.fixture
def make_test_conditions():
    # tmp_ws = temperary_workspace
    tmp_ws.mkdir()
    should_return_true_too.mkdir()
    should_return_false_too.mkdir()
    mk_these = [
        Path(should_return_true_too / "a_file.sh"),
        Path(should_return_true_too / "a_file2.bash"), 
        Path(should_return_true_too /"a_file3.zsh"),
        Path(should_return_true_too /"a_file4.tar.gz"),
        Path(should_return_true_too /"setup"),
        Path(should_return_true_too / "install"),
        Path(should_return_false_too / "code.py"),
        Path(should_return_false_too / "c++.cpp")
        ]
    for mock_file in mk_these:
        mock_file.touch()

# make sure is_download_from_terminal returns true for all inputs that it should do so for:
@pytest.mark.parametrize(
    "path_to_a_file, expected_bool",
    [
        # True cases
        (Path(should_return_true_too / "a_file.sh"), True),
        (Path(should_return_true_too / "a_file2.bash"), True),
        (Path(should_return_true_too / "a_file3.zsh"), True),
        (Path(should_return_true_too / "a_file4.tar.gz"), True),
        (Path(should_return_true_too / "setup"), True),
        (Path(should_return_true_too / "install"), True),

        # False cases
        (Path(should_return_false_too / "code.py"), False),
        (Path(should_return_false_too / "c++.cpp"), False),
    ]
)
def test_is_download_from_terminal1(make_test_conditions, path_to_a_file, expected_bool):
    created = [Path('/Users/parvinnourian/Projects/tmp_ws')]
    try:
        assert is_download_from_terminal(path_to_a_file) == expected_bool
    finally:
        cleanup(created)
