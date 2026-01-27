from pathlib import Path
from .foldproHelpers import (atomicCopyError, inValidInputError,
                            partiallyOrganizedError, nonAtomicMoveError, wrongOSError, noPathGivenError)
import sys
from typing import Optional, Tuple
import shutil
import re
from rich import print
import argparse




# ============================================================================
# ERROR HANDLING
# ============================================================================

ERROR_MESSAGES = {
    partiallyOrganizedError: lambda e: (
        f"Foldpro ran into a {e.errorCause.__class__.__name__} while organizing your files."),
    nonAtomicMoveError: lambda e: (
        f"Foldpro ran into a {e.errorCause.__class__.__name__} while moving {str(e.dest)} to final destination.",
    ),
    atomicCopyError: lambda e: (
        f"Foldpro ran into a {e.errorCause.__class__.__name__} while copying {e.userFolderCopy}."
    )
}


def format_error_message(description: str, commands: list[str], is_special: bool = False) -> str:
    """Format error message with optional cleanup commands."""
    lines = []
    
    # Header
    if is_special:
        return ("\n[bold]Foldpro Exited.[/bold]")
    else:
        lines.append("[red]------ An Error Occurred ------[/red]")

    # Description
    lines.append(description)
    
    # Cleanup commands
    if commands:
        lines.append("To avoid issues in future runs, please run the following commands:")
        lines.append((" && ".join(commands) if len(commands) > 1 else commands[0]) + "\n")

    # Append Most common fixes if not special case
    if not is_special:
        lines.extend([
            "[cyan]Most Common Fixes:[/cyan]\n",
            "1. Go to: System Settings → Privacy & Security → Full Disk Access\n",
            "2. Turn the button for terminal on: [⚪────] --> [────🟢]\n",
            "3. IF the folder is in iCloud Drive, follow the steps here to store it locally on your mac: https://www.youtube.com/watch?v=wfX4rfVHY7s\n",
            "4. Restart Foldpro and try again."
        ])
    return ('\n'.join(f"[bold]{line}[/bold]" for line in lines)).rstrip()


def find_workspace() -> Optional[Path]:
    """Find workspace in /tmp. Returns None if not found or permission error."""
    try:
        pattern = re.compile(r"^\.Foldpro-Workspace(\d{10})?$")
        return next(
            (p for p in Path("/tmp").iterdir() if p.is_dir() and pattern.match(p.name)),
            None
        )
    except (Exception, KeyboardInterrupt, SystemExit):
        return None


def cleanup_workspace(workspace: Optional[Path]) -> bool:
    """Clean workspace contents. Returns True if successful."""
    if not workspace:
        return True
    
    try:
        for item in workspace.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
        return True
    except (Exception, KeyboardInterrupt, SystemExit):
        return False


def get_error_info(exc: Exception) -> Tuple[str, str]:
    """Get error description for exception."""
    for error_type, handler in ERROR_MESSAGES.items():
        if isinstance(exc, error_type):
            return handler(exc)
    
    return (f"Foldpro ran into an unexpected {exc.__class__.__name__}.")


def cleanExit(func):
    """Handle all errors and ensure clean shutdown."""
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except KeyboardInterrupt:
            print("[bold]Foldpro exited.[/bold]")
            sys.exit(0)
        except noPathGivenError:
            print(
                "[red][bold]------ An Error Occurred ------[/bold][/red]\n"
                "[bold]No path was given.[/bold]"
                )
            sys.exit(1)
        except wrongOSError:
            print(
                "[red][bold]------ An Error Occurred ------[/bold][/red]\n"
                "[bold]Foldpro can only run on macOS.[/bold]"
                )
            sys.exit(1)
        except inValidInputError as exc:
            print(
                "[red][bold]------ An Error Occurred ------[/bold][/red]\n"
                f"[bold]{exc.errorMessage}[/bold]"
                )
            sys.exit(1)
        except (Exception, KeyboardInterrupt, SystemExit) as exc:
            # Determine if special case (KeyboardInterrupt)
            is_special = isinstance(exc, KeyboardInterrupt)
            
            # Get error description
            error_desc = get_error_info(exc)
            
            # Collect cleanup commands
            commands = []
            
            # Handle nonAtomicMoveError - try to delete partial move
            if isinstance(exc, nonAtomicMoveError):
                try:
                    if exc.dest.exists():
                        shutil.rmtree(exc.dest)
                except (Exception, KeyboardInterrupt, SystemExit):
                    commands.append(f"rm -rf {str(exc.dest)}")
            
            # Clean workspace
            workspace = find_workspace()
            if not cleanup_workspace(workspace):
                if workspace:
                    commands.append(f"rm -rf {workspace}")
                else:
                    commands.append("rm -rf /tmp/.Foldpro-Workspace*")
            
            # Print error message
            message = format_error_message(
                error_desc if not is_special else "",
                commands,
                is_special
            )
            print(message)
            
            sys.exit(1)
    
    return wrapper


def determineMode() -> Tuple[str, Path]:
    '''Parses the command given by the user.'''
    parser = argparse.ArgumentParser(description="A program to make organized copies of directories by file type.", prog="Foldpro", formatter_class=argparse.RawTextHelpFormatter, epilog="Example: python foldpro.py -m all")
    parser.add_argument('-m', '-mode', choices=['c', 'd', 'all', 'p', 'o'], help="""Tells Foldpro what mode you want it to run in
    Modes:
    ( c )   = Code files only
    ( d )   = Downloads from terminal only
    ( p )   = Pictures only
    ( o )   = Anything that isn't a code file or download
    ( all ) = Organizes your folder into everything. This is the default mode Foldpro will run in if you dont specify otherwise using -m.""")
    parser.add_argument('path', nargs='?', default=None, help="The path to the folder you would like Foldpro to organize(e.g. ~/Projects).")
    args = parser.parse_args()
    userFolder = args.path
    if userFolder is None:
        raise noPathGivenError()
    modeMap = {"c": "c_only", "d": "d_only", "o": "o_only", "all": "all", "p": "p_only", None: "all"}
    return modeMap[args.m], Path(args.path)
