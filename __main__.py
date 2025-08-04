from modules.manager import ProgramManager
WINDOW_CLASS_NAME: str = "GLWindow"
DRIVER_LOGGER: str     = "moderngl_window"
PROMPT: str            = ">>"
USAGE_MSG: str         = "Enter a command (or type 'help' for more information)."
EXIT_MSG: str          = "Exiting program..."

def init() -> ProgramManager:
    program = ProgramManager(__file__, WINDOW_CLASS_NAME, DRIVER_LOGGER)
    print(program.load_windows())
    return program

def main():
    program = init()
    print(USAGE_MSG)
    while program.should_run():
        output = None
        program.get_input(PROMPT)
        command = program.find_command()
        if command == None:
            output = '\n'.join([ f"Command '{program.last_command()}' does not exist.", USAGE_MSG ])
        elif not program.validate_command(command.usage):
            syntax = f"{program.last_command()} {str(command.usage)}".strip()
            output = f"Invalid command: did not adhere to syntax - {syntax}."
        else:
            output = command.cmd()
        if output != None: print(output)
    print(EXIT_MSG)

if __name__ == "__main__":
    main()