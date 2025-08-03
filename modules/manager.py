from typing import Callable
from modules.utils import  clear_screen, enable_logging, disable_logging

class CommandData():
    def __init__(self, usage: str, cmd: Callable):
        self.usage = usage
        self.cmd = cmd

class ProgramManager():
    def __init__(self, logger: str):
        self.running = True
        self.functions = CommandFunctions(self)
        self.logger = logger
    def find_command(self, input: list) -> Callable | None:
        if(input[0] == ""):
            return None
        for key, value in self.functions.COMMANDS.items():
            if(input[0] == key):
                return value.cmd
        return None
    def stop(self):
        self.running = False
    def should_run(self):
        return self.running

class CommandFunctions():
    def run(self):
        print("run")
    def spawn(self):
        print("spawned")
    def clear(self):
        clear_screen()
    def template(self):
        print("templated")
    def log(self):
        enable_logging(self.program.logger)
        print(f"Successfully enabled driver logs for {self.program.logger}.")
    def nolog(self):
        disable_logging(self.program.logger)
        print(f"Successfully disabled driver logs for {self.program.logger}.")
    def help(self):
        for key, value in self.COMMANDS.items():
            print(f"{key} - {value.usage}")
    def exit(self):
        self.program.stop()

    def __init__(self, program: ProgramManager):
        self.program = program
        self.COMMANDS = {
            "run":      
                CommandData(
                    "Run desired program.",
                    self.run
                ),
            "spawn":
                CommandData(
                    "Spawn a new program folder based on a template.",
                    self.spawn
                    ),
            "clear":
                CommandData(
                    "Clear the terminal screen.",
                    self.clear
                    ),
            "template":
                CommandData(
                    "Create a new template based on an existing project folder",
                    self.template
                ),
            "log":
                CommandData(
                    "Run desired program.",
                    self.log
                ),
            "nolog":
                CommandData(
                    "Run desired program.",
                    self.nolog
                ),
            "help":
                CommandData(
                    "Run desired program.",
                    self.help
                ),
            "exit":
                CommandData(
                    "Exit this application.",
                    self.exit
                )
        }