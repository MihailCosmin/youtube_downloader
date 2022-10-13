import yt_dlp

from althomcodebase import get_object_attributes
from althomcodebase import get_object_methods

dl_ops = {
    'print_help': True,
}

ydl = yt_dlp.YoutubeDL(dl_ops)

ydl.evaluate_outtmpl()

# print(ydl.params)


print(get_object_methods(ydl))