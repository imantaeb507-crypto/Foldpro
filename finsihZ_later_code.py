def pre_is_dir_and_exists(p: Path) -> Union[type[bool], str]:
    def istransversable(path: Path) -> Union[bool, str]:
        """
        Return True if all ancestor directories of `path` exist and have execute (traverse) permission.
        Return False if any ancestor does not exist.
        Return an error-message string (err_msg) if an ancestor exists but lacks execute permission.
        """

    # iterate ancestors from root down to immediate parent
    for ancestor in reversed(path.parents):
        if not ancestor.exists():
            return False
        if not os.access(str(ancestor), os.X_OK):
            err_msg = f'''
In order For Foldpro to work, it needs to have execute permmision on {ancestor.name!s}.
To give it that(and to restart the program) run the following:
chmod '''
            return err_msg

    return True
    pass


#TODO:Get pre_is_dir_and_exists() written:
'''
-Determine under what conditions your code is going to be under and adjust all of the following in accordance wiht that new understanding
-Define desired inputs and outputs:
    *INPUTS: The normlized path object
    *OUTPUTS: True if all goes well or an error message telling about what command they should run in order to fix the issue and restart the program, should return false
-Define how you want it to integrate/behave with prompt with path
    *I want it to be pre-requste for is_dir() and exists() running
    *If the return value of pre_is_dir_and_exists() is an error message, I want the error message displayed and for the program to exit
    *if pre_is_dir_and_exists() returns false only, I want the program to wait for another path prompt
-Define everything that needs to be checked(list it out)
    *Is every folder tranversable
    *Do I have read permmision on the last folder?
-Figure out how to account for extremly unlikely but possible errors that were accounted for in your code
'''
