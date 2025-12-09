from pathlib import Path
import shutil


def cleanup(delete_these: list[Path]):
    for entree in delete_these:
        if entree.is_file():
            entree.unlink()
        elif entree.is_dir():
            shutil.rmtree(str(entree))

