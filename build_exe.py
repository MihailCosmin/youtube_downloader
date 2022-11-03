from os import walk
from os import system
from os import listdir
from os import remove
from os import chmod
from os.path import dirname
from os.path import join

from stat import S_IWRITE

from time import sleep

from shutil import rmtree
from shutil import move

system("python setup.py build")

print("Finished building")

print("Starting clean-up")

with open('files.txt', 'r', encoding="utf-8") as _:
    build_list = _.readlines()

build_list = [file.replace("\n", "") for file in build_list]

missing_dir = False

root_dir = dirname(__file__)
for root, dirs, files in walk(join(root_dir, "build")):
    for dir_ in dirs:
        if not missing_dir:
            missing_dir = join(root, dir_).replace(join(root_dir, "build"), "").split("\\")[1]
            missing_dir += "\\"
            print("will try to move lib")
            for _ in listdir(join(root_dir, "build", "lib")):
                move(
                    join(root_dir, "build", "lib", _),
                    join(root_dir, "build", missing_dir.replace("\\", ""), "src", _),
                )
            print("Moved lib")

        if missing_dir not in build_list:
            build_list.append(missing_dir)
        if dir_ != missing_dir.replace("\\", ""):
            dir_2 = join(root, dir_).replace(join(root_dir, "build", missing_dir), "").strip()
            if dir_2 not in build_list:
                try:
                    rmtree(join(root, dir_))
                except PermissionError:
                    try:
                        chmod(join(root, dir_), S_IWRITE)
                        sleep(1)
                        remove(join(root, dir_))
                    except PermissionError:
                        rmtree(join(root, dir_))
                print(f"Removed {join(root, dir_)}")

    for file in files:
        if not missing_dir:
            missing_dir = join(root, file).replace(join(root_dir, "build"), "").split("\\")[1]
            missing_dir += "\\"
        file2 = join(root, file).replace(join(root_dir, "build", missing_dir), "").strip()
        print(f"file2 {file2}")
        if file2 not in build_list:
            try:
                remove(join(root, file))
            except PermissionError:
                try:
                    chmod(join(root, file), S_IWRITE)
                    sleep(1)
                    remove(join(root, file))
                except PermissionError:
                    rmtree(join(root, file))
            print(f"Removed {join(root, file)}")

print("Finished clean-up")
