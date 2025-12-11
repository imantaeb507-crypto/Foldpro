# This module contains functions that two or more other packages of the program will use

from typing import Union, Optional
import os
import sys
import random
from pathlib import Path
import re
import time
from rich import print


# ---------------------------
# Exit and Fail helpers
# ---------------------------
class Exit:
    @staticmethod
    def fail(msg: str, fix_command: str = None):
        print(
            "============= Error ==============\n"
            f"FOLDPRO ERROR: {msg}", 
            file=sys.stderr
        )
        if fix_command:
            print(f"Shortcut to fix & retry:\n{fix_command}")
        sys.exit(1)

    @staticmethod
    def exit():
        print(
        "[bold]==================================[/bold]\n"
        "[bold]Thank you for considering FoldPro.[/bold]\n"
        "[bold]==================================[/bold]"
        )
        sys.exit()


class Formatter:
    '''
    I wanted this program to display messages in a consistent way that adapted to the mode the user is in.
    To accomplish that, I wrote this class.
    '''
    def __init__(self, header):
        self.header = header

    def format(self, *lines):
        formatted_message = [f"[bold]{self.header}[/bold]\n"]
        for line in lines:
            formatted_message.append(f"[bold]{line}[/bold]\n")
        return ( "".join(formatted_message).rstrip())
    
    


# User options that Foldpro will use for memebership checks:
YES = {'yes', 'yep', 'yup', 'y', 'yrp', 'mhmm'}
NO = {'no', 'n', 'nope', 'nah', 'nahh'}
EXIT = {'e', 'exit', 'q', 'quit'}



foldpro_exit = Exit.exit

# Makes however many random digits you tell it too:
def mk_random(amount_of_digits: int) -> str:
    digits = []
    for i in range(amount_of_digits):
        digits.append(str(random.randint(0,9)))
    digits = ''.join(digits)
    return digits


