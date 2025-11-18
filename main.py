from typing import type
'''
This program organizes the folder you give it into 4 folders:
-a 'Pictures' folder for pictures in the directory
-a 'Code Files' folder for all the code files
-a 'Downloads From Terminal' folder for packages or libarys you downloaded from your computer
-a 'Others' folder for files that dont either 3 of the categorys mentioned above
It does this by making a COPY of the folder that you give it, and then reading all the file
names in that folder and organizing them according to their file extensions.
This program, currently, will work for macOS, Linux and Windows.
'''



def main() -> type[None]:
    pass





'''
TODO:
    add a corrects_names() function at the end of the program in order to  get
    the folders in their correct names. Correct names:
    -'Photos'
    -'Code Files'
    -'Downloads From Terminal'
    -Others
TODO:
    - Make it so that brew refuse's to download Foldproif the system being used isnt macOS and or if the fielsystem being used isnt APFS
    - make sure that each and every line of text Foldpro prints flush's left. And, for those print message that use multiple lines make it so that the print statement that tells to print them is in a readable format and that there are no extra lines above or below the message
    - When you think all the code for Foldpro has been written, go throguh the entire thing and figure out hwo to simplify the user experience even more
    - Make sure each and every message that could be printed to the user sounds freindly, is readable, and isnt longer than it need be.
    - Leave a helpful and pithy comment on every function in all modules filled with all the information you think is most important to the fucntoin
    - make it so that each and eveyr message that can be printed by foldpro that expects and sort of input from the user has the > sighn flsuhed left at the bottom of the message. Make it so that this sighn is specificed by a print statement: never the input  statement.
    - On the website where you provide documentation for Foldpro, tell about how they need to run Foldpro with sudo in order for it too run
    - make sure all of the input statements have .strip() somewhere in them
    - when packaging it into brew make it so that brew refuses to install macOS Yosemite (10.10) or later is being used
    - make it so that every parameter in which's place a path object is supposed to go has the name 'p'. 
    - make sure all terminal fix commands work for most shell terminals(if possible).
    - make it so that every input() statement has .strip() and .lower()
    - somehow ensure that a user has a reliable version of python that can has eveything needed in order to run Foldpro
    - Make all the arrows that the program CAN show in messages those little arrows that chatGPT produces and not the messy ones you makes using - and >
'''
