from pathlib import Path
import re
import glob
from typing import Tuple, Optional
import os
from Helpers import Exit, Formatter, YES, NO, EXIT, mk_random
from rich.traceback import install
from rich import print
install()
setup_formatter = Formatter("[yellow]====================================== Setup ======================================[/yellow]")
fail = Exit.fail
foldpro_exit = Exit.exit






# ---------------------------
# Functionality 1; Setup
# ---------------------------


def set_up_workspace() -> Tuple[Path, Path]:
   '''
   Makes Foldpro's workspace(if it dosent exist yet) and it's necessary sub-folders.
   '''
   def _make_workspace() -> Tuple[Path, Path]:
       # In the extremly rare case that /tmp/Foldpro-Workspace with 15 random numbers appended to the name also exists under tmp, Foldpro will continue to attempt to make a unique folder under tmp:
       while True:
           random_15_digits = mk_random(15)
           try:
               workspace = Path(f"/tmp/Foldpro-Workspace{random_15_digits}")
               workspace.mkdir()
               break
           except FileExistsError:
               continue
       history_dir = workspace / 'history_dir'
       folder_copies = workspace / 'tmp_folder_copies'
       history_dir.mkdir()
       folder_copies.mkdir()
       return folder_copies, history_dir
  
   # Find the already existing workspace(if there is one):
   pattern = re.compile(r"^Foldpro-Workspace\d{15}$")
   matches = [Path(p) for p in Path("/tmp").iterdir() if p.is_dir() and pattern.match(p.name)]




   # If there already is a workspace, simply return it's subfolders:
   if matches:
       folder_copies = matches[0] / 'tmp_folder_copies'
       history_dir = matches[0] / 'history_dir'
       return folder_copies, history_dir
  
   # If not, make it, and then return its newly created subfolders:
   else:
       return _make_workspace()
  


  




def set_up_instructions():
   '''
   Guides user through setup proccess
   '''


   print(setup_formatter.format(
   "1. Go to: System Settings --> Privacy & Security --> Full Disk Access\n"
   "\n"
   "2. Turn the botton for terminal on: [⚪────] --> [────🟢]\n"
   "\n"
   "3. IF you want to organize iCloud folders, move them to your local drive so Foldpro can work on them.\n"
   "   How To Do That: https://www.youtube.com/watch?v=wfX4rfVHY7s&t=95s\n\n"


   "Type 'd' to move on."
   ))


   while True:
       feedback = input('>').strip().lower()
       if feedback in {'d', 'done'}:
           return
       elif feedback in EXIT:
           foldpro_exit()
       else:
           print(setup_formatter.format(
           "Input not understood. Reply 'd' for done or 'e' to exit."
           ))


def setup_instructions_wrapper() -> type[None]:
   '''
   Introduces user to Foldpro and walks them through setup proccess
   '''
  
   print('\n')
   print(setup_formatter.format(
   "Thanks for choosing FoldPro! Before we begin, we just need to perform a little setup.\n"
   "Please be warned that if these setup instructions aren't followed Foldpro might act unpredictably.\n"
   "Enter 'e' at any time to exit.\n\n"
   "Begin Setup? (y/n)"
   ))


   while True:
       choice = input('>').strip().lower()


       if choice in YES:
           return set_up_instructions()


       elif choice in NO:
           print(setup_formatter.format(
           "What would you like to do, then:\n"
           "- Begin setup (S)\n"
           "- Exit Program (E)"
           ))
           while True:
               sub_choice = input('>').strip().lower()
               if sub_choice in EXIT:
                   foldpro_exit()
               elif sub_choice in {'s', 'setup', 'begin setup'}:
                   return set_up_instructions()
               else:
                   print(setup_formatter.format(
                   "Input not understood. Reply 'b' for begin setup or 'e' to exit."
                   ))


       elif choice in EXIT:
           foldpro_exit()


       else:
           print(setup_formatter.format(
           "Input not understood. Reply 'y' for begin setup or 'e' to exit."
           ))



class Setup:
   # Full setup: Will only ever run once in the beginning, when the user first runs the program:
   @staticmethod
   def full_setup() -> Tuple[Path, Path]:
       setup_instructions_wrapper()
       return set_up_workspace
   # runs when the program just wants to get the workspace subfolder paths:
   @staticmethod
   def get_workspace_subfolders() -> Tuple[Path, Path]:
       return set_up_workspace
   



#TODO: get all the preflight operations modulated, tested, and then put into the preflight class
#  - Test all of them isolated and then togetor
#  - Integrate into __enter__
#  - Get ChatGPT to give you the errors list 
#  - Get that integrated into all of the functionality and anything that might need to go along with it
#  - Integrate the whole thing into typer



'''
Tested already:
  - All of setup module
  - canonical_version from Helpers



'''
