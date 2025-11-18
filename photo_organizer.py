import shutil
from pathlib import Path

def photo_organizer(copied_version):
    global things_wrong
    # Find Pictures folder (case-insensitive). Create it if not found for safety.
    pictures_folder = next(
        (p for p in copied_version.iterdir() if "pictures" in p.name.lower() and p.is_dir()),
        None
    )

    image_extensions = {
        "jpg", "jpeg", "png", "gif", "bmp", "tiff", "tif",
        "heic", "heif", "webp", "cr2", "nef", "arw", "dng", "svg"
    }

    # Snapshot files first to avoid rglob changing under us while we move files
    candidates = [p for p in copied_version.rglob("*") if p.is_file()]

    for item in candidates:
        # skip files already in the pictures folder (avoid moving them again)
        if pictures_folder in item.parents:
            continue

        if item.suffix.lower().lstrip(".") in image_extensions:
            # Build destination path and ensure it is unique (avoid overwriting)
            dest = pictures_folder / item.name
            if dest.exists():
                stem = item.stem
                suf = item.suffix
                i = 1
                while (pictures_folder / f"{stem}_{i}{suf}").exists():
                    i += 1
                dest = pictures_folder / f"{stem}_{i}{suf}"

            shutil.move(str(item), str(dest))  # move file (use str() for max compatibility)





