import os
import shutil
import logging
import importlib.util

def dict_empty(dictionary: dict) -> bool:
    return not bool(dictionary)

def get_folder(path: str) -> str:
    return os.path.dirname(os.path.normpath(os.path.abspath(path)))

def get_all_subfolders(path: str) -> list[str]:
    dirs: list[str] = []
    for file in os.listdir(path):
        file = os.path.normpath(f"{path}/{file}")
        if os.path.isdir(file): dirs.append(file)
    return dirs

def get_basename(path: str) -> str:
    return os.path.basename(os.path.normpath(path))

def file_exists(path: str) -> bool:
    return os.path.exists(path)

def recursive_copy(src: str, dest: str):
    shutil.copytree(src, dest)

def disable_logging(name: str):
    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.propagate = False
    logger.addHandler(logging.NullHandler())

def enable_logging(name: str):
    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.propagate = True

def add_abs_path(file: str, path: str) -> str:
    return f"{os.path.normpath(os.path.dirname(os.path.abspath(file)))}/{path}"

def import_window_class(path: str, windowClass: str):
    path = os.path.abspath(path)
    moduleName = os.path.splitext(os.path.basename(path))[0]

    spec = importlib.util.spec_from_file_location(moduleName, path)
    if spec == None or spec.loader == None:
        raise ImportError(f"Failed to load module from {path}.")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if not hasattr(module, windowClass):
        raise AttributeError(f"No class '{windowClass}' found in {path}.")
    return getattr(module, windowClass)

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')