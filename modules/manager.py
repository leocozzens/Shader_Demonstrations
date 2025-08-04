from typing import Callable
import modules.utils as util
from modules.window import ProgramWindow

RELATIVE_APP_PATH:str         = "/app.py"
RELATIVE_PROGRAM_FOLDER: str  = "/programs"
RELATIVE_TEMPLATE_FOLDER: str = "/templates"

HELP_PREFACE:str = "Command syntax is displayed below, the first letter of each command may be used as a shortcut."

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
        util.disable_logging(logger)
        self.programFolder = util.get_folder(programFile)
        self.windowClass = windowClass
        self.logger = logger

        self.running = True
        self.functions = CommandFunctions(self)
        self.input: list[str] = [ "" ]
        self.windows: dict[str, ProgramWindow] = {}
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
                windowResults.append(str(e))
        if util.dict_empty(self.windows):
            windowResults.append("No window programs loaded.")
        return '\n'.join(windowResults)
    def get_input(self, prompt: str):
        inputData = input(prompt + ' ').strip()
        self.input = inputData.split(' ')
        self.input[0] = self.input[0].lower()
    def find_command(self) -> CommandData | None:
        if self.input[0] == "":
            return None
        for key, value in self.functions.COMMANDS.items():
            if self.input[0] == key or self.input[0] == key[0]:
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
        name = self.program.input[1]
        if name not in self.program.windows.keys():
            return f"No GLWindow with name '{name}' found."
        self.program.windows[name].run()
        return f"Successfully ran and exited GLWindow located in '{name}'."
    def enumerate(self) -> str | None:
        prepender = '- '
        programs = [ prepender + program for program in self.program.windows.keys()]
        templates = util.get_all_subfolders(f"{self.program.programFolder}{RELATIVE_TEMPLATE_FOLDER}")
        templates = [ prepender + util.get_basename(template) for template in templates ]
        return '\n'.join([
            "Enumeration Results:",
            "{:-^50s}".format("Window Programs"),
            *programs,
            "{:-^50s}".format("Existing Templates"),
            *templates
        ])
    def update(self) -> str | None:
        self.program.windows.clear()
        return "Wiped windows from memory.\n" + self.program.load_windows()
    def spawn(self) -> str | None:
        templateName = self.program.input[1]
        templatePath = f"{self.program.programFolder}{RELATIVE_TEMPLATE_FOLDER}/{templateName}"
        programName = self.program.input[2]
        programPath = f"{self.program.programFolder}{RELATIVE_PROGRAM_FOLDER}/{programName}"
        if not util.file_exists(templatePath):
            return f"No template with name '{templateName}' could be found."
        if util.file_exists(programPath):
            return f"Program with name '{programName}' already exists"
        try:
            util.recursive_copy(templatePath, programPath)
        except Exception as e:
            return f"Failed to create new program '{programName}' from '{templateName}' template: {str(e)}"
        return (
            f"Successfully created new program '{programName}' from '{templateName}' template.\n"
            "Please update cache with 'update'."
        )
    def template(self) -> str | None:
        programName = self.program.input[1]
        programPath = f"{self.program.programFolder}{RELATIVE_PROGRAM_FOLDER}/{programName}"
        templateName = self.program.input[2]
        templatePath = f"{self.program.programFolder}{RELATIVE_TEMPLATE_FOLDER}/{templateName}"
        if not util.file_exists(programPath):
            return f"No program with name '{programName}' could be found."
        if util.file_exists(templatePath):
            return f"Template with name '{templateName}' already exists"
        try:
            util.recursive_copy(programPath, templatePath)
        except Exception as e:
            return f"Failed to create new template '{templateName}' from '{programName}' program: {str(e)}"
        return f"Successfully created new template '{templateName}' from '{programName}' template."
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
        text.insert(0, HELP_PREFACE)
        return '\n'.join(text)
    def clear(self) -> str | None:
        util.clear_screen()
        return None
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
            "template":
                CommandData(
                    "Create a new template based on an existing project folder.",
                    CommandUsage("<program> <template>", 2, 2),
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
            "clear":
                CommandData(
                    "Clear the terminal screen.",
                    NO_ARGS,
                    self.clear
                ),
            "quit":
                CommandData(
                    "Quit this application.",
                    NO_ARGS,
                    self.quit
                )
        }