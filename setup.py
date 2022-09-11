from cx_Freeze import setup, Executable
from sys import platform
 
base = None
# uncomment below lines to hide command prompt
# tqdm prints to command prompt so it needs to be removed for the program to run
# Important: if you hide the console, make sure your scripts don't try to print anything, otherwise they might not work as expected
if (platform == "win32"):
    base = "Win32GUI"
 
executables = [Executable("main.py", base=base, icon="icons/yt_dlp_gui.png")]
 
packages = ["ctypes","imp", "PySide2", "yt_dlp"]
excludes = ["PyQt5", "PyQt4", "reportlab", "matplotlib", "numba", "scipy", "sqlalchemy", "sqlite3", "soupsieve", "llvmlite", "black", "bs4", "jupyter", "tornado", "pygments"]
options = {
    'build_exe': {
        'packages': packages,
        'excludes': excludes, 
    },
}
setup(
    name="<yt_dlp_gui>",
    options=options,
    version="0.0.0.1",
    description='<yt_dlp_gui is a standalone application for '
                + 'running simple automations for EFW IPC and SRM.'
                + 'Printing, checking etc.>',
    executables=executables
    )
# Run this to create the exe:
# python setup.py build
#
# Then copy the res folder in the same folder as the .exe