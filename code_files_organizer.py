from pathlib import Path
import shutil

def code_files_organizer(copied_version: Path):
    global things_wrong
    # The extensions were looking to identify in file names in order to classify it as a code file or not:
    code_extensions = [
        "py", "pyw", "ipynb",       # Python
        "js", "ts", "jsx", "tsx",   # JavaScript / TypeScript
        "java", "class",             # Java
        "c", "cpp", "cxx", "h",     # C/C++
        "cs",                        # C#
        "rb",                        # Ruby
        "php", "php3", "php4", "php5",
        "go",                        # Go
        "swift",                     # Swift
        "kt", "kts",                 # Kotlin
        "scala",                     # Scala
        "m", "mm",                   # Objective-C
        "rs",                        # Rust
        "sh", "bash", "zsh", "ksh", # Shell scripts
        "r",                         # R
        "pl", "pm",                  # Perl
        "sql",                       # SQL
        "xml", "json", "yaml", "yml" # Configuration / markup files often treated as code
    ]
    
    # The following finds and organizes code files in a directory into the Code Files directory
    for file_path in main_data[0].rglob("*"):
        if file_path.is_file():
            # Compare file extension ignoring case
            if file_path.suffix.lower().lstrip(".") in code_extensions:
                try:
                    # Move file into the Code Files folder
                    shutil.move(str(file_path), code_folder / file_path.name)
                except Exception as e:
                    # Catch unexpected errors per file to continue processing
                    things_wrong.append(f"Warning: Could not move {file_path}: {e}")

