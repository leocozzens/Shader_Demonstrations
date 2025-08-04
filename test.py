import os

def get_all_subdirs(path: str) -> list[str]:
    dirs: list[str] = []
    for file in os.listdir(path):
        file = f"{path}/{file}"
        if os.path.isdir(file): dirs.append(file)
    return dirs

def get_parent_folder(path: str):
    return os.path.dirname(os.path.abspath(path))

dirs = get_all_subdirs(get_parent_folder(__file__) + "\\templates" )

for i in dirs:
    print(i)