from pathlib import Path
import re
from typing import Tuple
from FoldproHelpers import Exit, Formatter, YES, NO, EXIT, mk_random
from rich.traceback import install
from rich import print
install()
setup_formatter = Formatter("[yellow]====================================== Setup ======================================[/yellow]")
fail = Exit.fail
foldpro_exit = Exit.exit


def set_up_workspace() -> Tuple[Path, bool]:
   '''
   Makes Foldpro's workspace(if it dosent exist yet). This is where temporary folder copies will go to get organized.
   '''

   # This function figure out wether this is the first time a Foldpro command is running on a Users computer as part of its main task.
   # To make this information available for setup_instructions_wrapper(), 
   # I store it in this variable and return it as the last value so the other function can behave correctly.
   has_already_ran = False
   def _make_workspace() -> Tuple[Path, bool]:
       # In the extremly rare case that /tmp/Foldpro-Workspace with 15 random numbers appended to the name also exists under tmp, Foldpro will continue to attempt to make a unique folder under tmp:
       while True:
           random_15_digits = mk_random(15)
           try:
               workspace = Path(f"/tmp/Foldpro-Workspace{random_15_digits}")
               workspace.mkdir()
               break
           except FileExistsError:
               continue
       return workspace, has_already_ran


   # Find the already existing workspace(if there is one):
   pattern = re.compile(r"^Foldpro-Workspace\d{15}$")
   matches = [Path(p) for p in Path("/tmp").iterdir() if p.is_dir() and pattern.match(p.name)]




   # If there already is a workspace, return it's path as a path object:
   if matches:
       has_already_ran = True
       workspace = matches[0]
       return workspace, has_already_ran
  
   # If not, make it, and then return it's path object:
   else:
       return (_make_workspace())
  

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


   "Type 'd' when done."
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


def setup_instructions_wrapper() -> None:
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



def setup():
    workspace, has_already_ran = set_up_workspace()
    if not has_already_ran:
        setup_instructions_wrapper()
    return workspace
