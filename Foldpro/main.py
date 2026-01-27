from .overallFlow import cleanExit, determineMode
from .foldproMainFunctionality import foldproMainFunctionality
from .foldproHelpers import wrongOSError
import platform
from .preflightOperations import preFlightOperations
from rich import print

@cleanExit
def main():
    if platform.system() != 'Darwin':
        raise wrongOSError()
    mode, userFolder = determineMode()
    userFolderCopy = preFlightOperations(userFolder)
    finalDest = foldproMainFunctionality(mode=mode, userFolderCopy = userFolderCopy)
    print(f"[bold]Folder [green]{finalDest.name}[/green] has been organized and can be found at ~/Foldpro Copies.[/bold]")

if __name__ == '__main__':
    main()
