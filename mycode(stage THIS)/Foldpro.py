# TODO: Write high-level description of this module once you've written the code.

# TODO: Import necessary modules here:
from FoldproHelpers import Formatter, YES, NO, EXIT
import sys
from preflight_operations import get_path_and_copy, setup
import major_functions
import re
from pathlib import Path
import shutil

# All header objects except for the one used in setup.py
home_header = Formatter(header="Home", header_color="orange")
code_file_header = Formatter(header="Code Files", header_color="red")
pictures_header = Formatter(header="Pictures", header_color="blue")
downloads_header = Formatter(header="Downloads from Terminal", header_color="green")
others_header = Formatter(header="Others", header_color="magenta")
everything_header = Formatter(header="Everyting", header_color="yellow")

class FoldproCommands:
    def __init__(self):
        pass

    @staticmethod
    def code_files_only():
        workspace = setup()
        while True:
            workspace = get_path_and_copy(code_file_header, workspace)
            global CODE_FILES
            global files
            cleanup_data = major_functions.Helper_functions.name_collison_prevention(workspace)


            CODE_FILES = major_functions.Helper_functions.makes_folders(folder_names = ['Code Files'], parent_path = workspace)
            _, files = major_functions.Helper_functions.categorize_files_and_symlinks(workspace)
            major_functions.organize(files = files, CODE_FILES = CODE_FILES, mode = 'code_files_only')
            major_functions.finalize_state(cleanup_data = cleanup_data, workspace = workspace, CODE_FILES = CODE_FILES)


    @staticmethod
    def pictures_only():
        workspace = setup()
        while True:
            workspace = get_path_and_copy(pictures_header, workspace)
            global PICTURES
            global files
            cleanup_data = major_functions.Helper_functions.name_collison_prevention(workspace)

            PICTURES = major_functions.Helper_functions.makes_folders(folder_names = ['Pictures'], parent_path = workspace)
            _, files = major_functions.Helper_functions.categorize_files_and_symlinks(workspace)
            major_functions.organize(files = files, PICTURES = PICTURES, mode = 'pictures_only')
            major_functions.finalize_state(cleanup_data = cleanup_data, workspace = workspace, PICTURES = PICTURES)


    @staticmethod
    def downloads_only():
        workspace = setup()
        while True:
            workspace = get_path_and_copy(downloads_header, workspace)
            global DOWNLOADS_FROM_TERMINAL
            global files
            cleanup_data = major_functions.Helper_functions.name_collison_prevention(workspace)

            DOWNLOADS_FROM_TERMINAL = major_functions.Helper_functions.makes_folders(folder_names = ['Downloads From Terminal'], parent_path = workspace)
            _, files = major_functions.Helper_functions.categorize_files_and_symlinks(workspace)
            major_functions.organize(files = files, DOWNLOADS_FROM_TERMINAL = DOWNLOADS_FROM_TERMINAL, mode = 'downloads_only')
            major_functions.finalize_state(cleanup_data = cleanup_data, workspace = workspace, DOWNLOADS_FROM_TERMINAL = DOWNLOADS_FROM_TERMINAL)
    @staticmethod
    def others_only():
        workspace = setup()
        while True:
            workspace = get_path_and_copy(others_header, workspace)
            global OTHERS
            global files
            cleanup_data = major_functions.Helper_functions.name_collison_prevention(workspace)

            OTHERS = major_functions.Helper_functions.makes_folders(folder_names = ['Others'], parent_path = workspace)
            _, files = major_functions.Helper_functions.categorize_files_and_symlinks(workspace)
            major_functions.organize(files = files, OTHERS = OTHERS, mode = 'others_only')
            major_functions.finalize_state(cleanup_data = cleanup_data, workspace = workspace, OTHERS = OTHERS)

    @staticmethod
    def everything():
        workspace = setup()
        while True:
            workspace = get_path_and_copy(home_header, workspace)
            global PICTURES
            global CODE_FILES
            global DOWNLOADS_FROM_TERMINAL
            global OTHERS
            global files
            cleanup_data = major_functions.Helper_functions.name_collison_prevention(workspace)


            PICTURES, CODE_FILES, DOWNLOADS_FROM_TERMINAL, OTHERS = major_functions.Helper_functions.makes_folders(
                folder_names = ['Pictures', 'Code Files', 'Downloads From Terminal', 'Others'],
                parent_path = workspace
            )
            symlinks, files = major_functions.Helper_functions.categorize_files_and_symlinks(workspace)
            major_functions.organize(
                files = files,
                symlinks = symlinks,
                PICTURES = PICTURES,
                CODE_FILES = CODE_FILES,
                DOWNLOADS_FROM_TERMINAL = DOWNLOADS_FROM_TERMINAL,
                OTHERS = OTHERS,
                mode = 'everything'
            )
            dest_of_organized_copy = major_functions.finalize_state(
                cleanup_data = cleanup_data,
                workspace = workspace,
                mode = 'everything'
            )
            print(everything_header.header(
                f"Folder '{workspace.name}' has been organized and can now be found at {str(Path.home() / str(dest_of_organized_copy))}."
                "Would you know like to organize another folder(o) or exit(e)?"))
            
            while True:
                choice = input('>').strip().lower()
                if choice in EXIT:
                    sys.exit()
                elif choice == 'o':
                    break
                else:
                    print(everything_header.header("Input not understood. Please respond with either 'o' for organize or 'e' for exit."))



class Foldpro_context_manager:
    '''
    This context manager makes it so that Foldpro exits cleanly no matter what unexpected error occurs.
    '''
    def __enter__(self):
        pass

    def __exit__(self, exc_type, *_):
        if exc_type in (KeyboardInterrupt, SystemExit):
            print(
            "[bold]==================================[/bold]\n"
            "[bold]Thank you for considering FoldPro.[/bold]\n"
            "[bold]==================================[/bold]"
            )
            sys.exit()
        elif exc_type is PermissionError:
            print("[bold red]Error:[/bold red] Permission denied. Please check your file permissions and try again.")
            sys.exit(1)
        elif exc_type is None:
            pass
        else:
            print(f"[bold red]An unexpected error occurred:[/bold red] {exc_type.__name__}: {exc_type.__doc__}")
            sys.exit(1)
        try:
            # delete any leftover workspace folders if they still exist:
            # This is done to ensure no leftover folders get left behind if the program comes across an unexpected error earlier on:
            pattern = re.compile(r"^Foldpro-Workspace(\d+)?$")

            matches = [
                p for p in Path("/tmp").iterdir()
                if p.is_dir() and pattern.match(p.name)
            ]
            if matches == []:
                return
            
            leftover_workspaces = [workspace for workspace in matches[0]]

            if leftover_workspaces == []:
                return

            for workspace in leftover_workspaces:
                try:
                    shutil.rmtree(workspace)
                except (PermissionError, OSError) as _:
                    # List the command the user should run in order to delete junk:
                    commands_to_run = []
                    for workspace in leftover_workspaces:
                        commands_to_run.append(f'rm -rf {str(workspace)}')
                    commands_to_run = ' && '.join(commands_to_run).rstrip()
                    print(
                    "Foldpro wasnt able to delete a few junk trailers due to some permmsision errors. Please run the following command in your terminal to fix this issue\n"
                    f"{commands_to_run}"
                    )
                leftover_workspaces.remove(workspace)
        except Exception as e:
            print(f"[bold red]An unexpected error occurred:[/bold red] {e.__name__}: {e.__doc__}")
            sys.exit(1)

                

def Foldpro():
    print(home_header.format(
    "How would you like too organize your folders? :",
    "* Into all categories(Code Files, Pictures, Downloads From Terminal, Others): e",
    "* Into one of the subcategorys(e.g.Pictures): sub"
    ))

    while True:
        desired_mode = input('>').strip().lower()
        if desired_mode in {'e', 'exit'}:
            sys.exit()
        if desired_mode in {'e'}:
            break
        elif desired_mode == 'sub':
            print(home_header.format(
            "Which one? :"
            "* Pictures: (p)",
            "* Code Files: (c)",
            "* Downloads From Terminal: (d)",
            "* Others: (o)"
            ))
            while True:
                subcategory_desicon = input('>').strip().lower()
                if subcategory_desicon in {'p', 'c', 'd', 'o'}:
                    break
                else:
                    print(home_header.format(
                        "Invalid input. Please enter one of the following options:"
                        "* Pictures: (p)",
                        "* Code Files: (c)",
                        "* Downloads From Terminal: (d)",
                        "* Others: (o)"))


            break

        else:
            print(home_header.format("Invalid input. Please enter one of the following options: e, p, c, d, o."))

    if desired_mode == 'e':
        FoldproCommands.everything()
    elif subcategory_desicon == 'p':
        FoldproCommands.code_files_only()
    elif subcategory_desicon == 'c':
        FoldproCommands.pictures_only()
    elif subcategory_desicon == 'd':
        FoldproCommands.downloads_only()
    elif subcategory_desicon == 'o':
        FoldproCommands.others_only()


Foldpro()
print("IT.FINNALY.WORKS!")

                                         








    










