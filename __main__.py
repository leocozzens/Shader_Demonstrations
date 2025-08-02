import modules.utils as util

# Constants
USAGE_MSG: str     = "Enter a command (or type 'help' for more information)"
DRIVER_LOGGER: str = "moderngl_window"

from pathlib import Path
import sys
import importlib.util

def import_module_from_path(filepath):
    filepath = Path(filepath).resolve()
    module_name = filepath.stem
    spec = importlib.util.spec_from_file_location(module_name, str(filepath))
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def main():
    print(USAGE_MSG)
    util.disable_logging(DRIVER_LOGGER)
    module = import_module_from_path(util.add_abs_path(__file__, "templates\\02_basic\\app.py"))
    module.NewWindow.run()

if __name__ == "__main__":
    main()