from cx_Freeze import setup, Executable
from sys import platform

base = None
if (platform == "win32"):
    base = "Win32GUI"

executables = [
    Executable(
        script="src/Youtube Downloader.py",
        base=base,
        icon="src/images/icons/youtube_downloader.ico"
    )
]

include_files = ["src/images/icons/youtube_downloader.ico"]
packages = ["ctypes", "imp", "PySide6", "yt_dlp", "cx_Freeze", "PyInstaller", "pyperclip", "regex", "adblockparser"]
excludes = [
    "PyQt5", "PyQt4", "reportlab", "matplotlib", "numba", "scipy", "sqlalchemy", "sqlite3", "soupsieve",
    "llvmlite", "black", "bs4", "jupyter", "tornado", "pygments"
]
options = {
    'build_exe': {
        'packages': packages,
        'excludes': excludes,
        'include_files': include_files,
    },
}

package_data = {
    '3rd': ['*'],
    'images': ['*', 'icons/*', 'images/*'],
    'themes': ['*'],
    'utils': ['*'],
    'widgets': ['*'],
    'ytb': ['*'],
}

setup(
    name="Youtube Downloader",
    packages=['utils', 'widgets', 'ytb', '3rd', 'images', 'themes'],
    package_dir={'': 'src'},
    package_data=package_data,
    options=options,
    version="0.0.2",
    description='Youtube Downloader is a Youtube Browser application based on PySide6 and yt-dlp.'
                + 'And it allows you to download single videos, playlists or queues.',
    executables=executables
)
