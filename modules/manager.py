from typing import Callable
import modules.utils as util
from modules.window import ProgramWindow

SUCCESSFUL_EXIT_MSG: str      = "Successfully exited program."
RELATIVE_APP_PATH:str         = "/app.py"
RELATIVE_PROGRAM_FOLDER: str  = "/programs"
RELATIVE_TEMPLATE_FOLDER: str = "/templates"

class CommandUsage():
    def __init__(self, syntax: str, min: int, max: int):
        self.syntax = syntax
        self.min = min
        self.max = max
    def __str__(self):
        return self.syntax

NO_ARGS = CommandUsage("", 0, 0)

class CommandData():
    Command = Callable[[], str | None]
    def __init__(self, about: str, usage, cmd: Command):
        self.about = about
        self.usage = usage
        self.cmd = cmd

class ProgramManager():
    def __init__(self, programFile: str, windowClass: str, logger: str):
        self.programFolder = util.get_folder(programFile)
        self.windowClass = windowClass
        self.logger = logger

        self.running = True
        self.exitMsg = SUCCESSFUL_EXIT_MSG
        self.functions = CommandFunctions(self)
        self.input: list[str] = [ "" ]

        self.windows: dict[str, ProgramWindow] = []
    def load_windows(self) -> str:
        windowResults: list[str] = []
        programFolders = util.get_all_subfolders(self.programFolder + RELATIVE_PROGRAM_FOLDER)
        for folder in programFolders:
            folderBase = util.get_basename(folder)
            try:
                newClass = util.import_window_class(folder + RELATIVE_APP_PATH, self.windowClass)
                self.windows[folderBase] = newClass
                windowResults.append(f"Succesfully loaded {self.windowClass} from {folderBase}.")
            except Exception as e:
                windowResults.append(e)
        if(util.dict_empty(self.windows)):
            windowResults.append("No windows loaded.")
        return '\n'.join(windowResults)
    def get_input(self, prompt: str):
        inputData = input(prompt + ' ')
        inputData = inputData.lower()
        self.input = inputData.split(' ')
    def find_command(self) -> CommandData | None:
        if(self.input[0] == ""):
            return None
        for key, value in self.functions.COMMANDS.items():
            if(self.input[0] == key):
                return value
        return None
    def last_command(self) -> str:
        return self.input[0]
    def validate_command(self, usage: CommandUsage) -> bool:
        inputLen = len(self.input) - 1
        if inputLen < usage.min or inputLen > usage.max:
            return False
        return True
    def stop(self):
        self.running = False
    def should_run(self) -> bool:
        return self.running
    def get_exit_msg(self) -> str:
        return

class CommandFunctions():
    def run(self) -> str | None:
        return "ran"
    def enumerate(self) -> str | None:
        if util.dict_empty(self.program.windows):
            return "No windows loaded."
        return '\n'.join(self.program.windows.keys())
    def update(self) -> str | None:
        return "updated"
    def spawn(self) -> str | None:
        return "spawned"
    def clear(self) -> str | None:
        util.clear_screen()
        return None
    def template(self) -> str | None:
        return "templated"
    def log(self) -> str | None:
        util.enable_logging(self.program.logger)
        return f"Successfully enabled driver logs for {self.program.logger}."
    def nolog(self) -> str | None:
        util.disable_logging(self.program.logger)
        return f"Successfully disabled driver logs for {self.program.logger}."
    def help(self) -> str | None:
        longest = max(len(key) + len(str(value.usage)) for key, value in self.COMMANDS.items())
        longest += 1
        text = [ f"{key + ' ' + str(value.usage):<{longest}} - {value.about}" for key, value in self.COMMANDS.items() ] 
        return '\n'.join(text)
    def quit(self) -> str | None:
        self.program.stop()
        return None

    def __init__(self, program: ProgramManager):
        self.program = program
        self.COMMANDS: dict[str, CommandData] = {
            "run":      
                CommandData(
                    "Run desired program.",
                    CommandUsage("<program>", 1, 1),
                    self.run
                ),
            "enumerate":      
                CommandData(
                    "List available programs.",
                    NO_ARGS,
                    self.enumerate
                ),
            "update":      
                CommandData(
                    "Update cache with current programs from disk.",
                    NO_ARGS,
                    self.update
                ),
            "spawn":
                CommandData(
                    "Spawn a new program folder based on a template.",
                    CommandUsage("<template> <program>", 2, 2),
                    self.spawn
                    ),
            "clear":
                CommandData(
                    "Clear the terminal screen.",
                    NO_ARGS,
                    self.clear
                    ),
            "template":
                CommandData(
                    "Create a new template based on an existing project folder.",
                    CommandUsage("<template> <program>", 2, 2),
                    self.template
                ),
            "log":
                CommandData(
                    "Enable driver logs printing to the terminal.",
                    NO_ARGS,
                    self.log
                ),
            "nolog":
                CommandData(
                    "Disable driver logs printing to the terminal.",
                    NO_ARGS,
                    self.nolog
                ),
            "help":
                CommandData(
                    "Request command information.",
                    NO_ARGS,
                    self.help
                ),
            "quit":
                CommandData(
                    "Quit this application.",
                    NO_ARGS,
                    self.quit
                )
        }