from os import walk
from os import system
from os import remove
from os.path import join

from shutil import rmtree

system("python setup.py build")

print("Finished building")

print("Starting clean-up")

with open('files.txt', 'r', encoding="utf-8") as _:
    build_list = _.readlines()

build_list = [file.replace("\n", "") for file in build_list]

for root, dirs, files in walk(r"C:\Users\munte\Downloads\Sync\Projects\yt_dlp_gui\build"):
    for dir_ in dirs:
        missing_dir = join(root, dir_).replace(r"C:\Users\munte\Downloads\Sync\Projects\yt_dlp_gui\build", "").split("\\")[1]
        missing_dir += "\\"
        if missing_dir not in build_list:
            build_list.append(missing_dir)
        if dir_ != missing_dir.replace("\\", ""):
            dir_2 = join(root, dir_).replace(join(r"C:\Users\munte\Downloads\Sync\Projects\yt_dlp_gui\build", missing_dir), "").strip()
            if dir_2 not in build_list:
                # print(f"{dir_2} not in {build_list}")
                rmtree(join(root, dir_))
    for file in files:
        missing_dir = join(root, file).replace(r"C:\Users\munte\Downloads\Sync\Projects\yt_dlp_gui\build", "").split("\\")[1]
        missing_dir += "\\"
        file2 = join(root, file).replace(join(r"C:\Users\munte\Downloads\Sync\Projects\yt_dlp_gui\build", missing_dir), "").strip()
        if file2 not in build_list:
            remove(join(root, file))

print("Finished clean-up")
