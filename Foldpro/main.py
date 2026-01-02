from overall_flow import determine_mode, after_organization_decision, clean_exit, MODE_HEADERS, is_macOS
from Foldpro_command import Foldpro_command
from preflight_operations import preflight_operations
from FoldproHelpers import WantsToExit

@clean_exit
def main():
    is_macOS()
    while True:
        mode_header = MODE_HEADERS[mode]
        user_folder_copy = preflight_operations(mode_header=mode_header)
        final_dest = Foldpro_command(mode=mode, user_folder_copy=user_folder_copy)
        
        decision = after_organization_decision(final_dest=final_dest, mode_header=mode_header)
        
        if decision == 'exit':
            raise WantsToExit
        elif decision == 'change':
            mode = determine_mode()
        # 'repeat' continues the loop automatically


if __name__ == '__main__':
    main()
