from os.path import dirname
from os.path import join
from althomcodebase import list_files

# TODO: Folder names also need to be added to the list
with open(join(dirname(dirname(__file__)), "files.txt"), "w", encoding="utf-8") as _:
    for keep in list_files("build/exe.win-amd64-3.9/lib"):
        _.write(f'{keep.replace("build/exe.win-amd64-3.9/", "")}\n')
