import os
import sys
import logging
import importlib.util

def disable_logging(name: str) -> None:
    logging.getLogger(name).addHandler(logging.NullHandler())

def enable_logging(name: str) -> None:
    logging.getLogger(name).handlers.clear()

def import_window_class(path: str, class_name: str):
    # Ensure it's an absolute path to a .py file
    path = os.path.abspath(path)
    module_name = os.path.splitext(os.path.basename(path))[0]

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load module from {path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)

    # Grab the class
    if not hasattr(module, class_name):
        raise AttributeError(f"No class '{class_name}' found in {path}")
    return getattr(module, class_name)

def add_abs_path(file: str, path: str) -> str:
    return f"{os.path.dirname(os.path.abspath(file))}\\{path}"

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')