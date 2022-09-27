from os.path import join
from os.path import expanduser

import yt_dlp

class YoutubeDLP():
    """YoutubeDLP
    https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/options.py
    
    Options:
        throttled-rate: str
        limit-rate: str
        retries: int
        file-access-retries: int
        fragment-retries: int
        retry-sleep: int
        skip-unavailable-fragments: bool
        abort-on-unavailable-fragment: bool
        keep-fragments: bool
        no-keep-fragments: bool
        buffer-size: str
        resize-buffer: bool
        no-resize-buffer: bool
        http-chunk-size: str
        test: bool
        playlist-reverse: bool
        no-playlist-reverse: bool
        playlist-random: bool
        lazy-playlist: bool
        no-lazy-playlist: bool
        xattr-set-filesize: bool
        hls-prefer-native: bool
        hls-prefer-ffmpeg: bool
        hls-use-mpegts: bool
        download-sections: bool
        downloader: dict
        downloader-args: dict
        
    Workarounds:
        encoding: str
        legacy-server-connect: bool
        no-check-certificates: bool
        prefer-insecure: bool
        user-agent: str
        referer: str
        add-header: str
        bidi-workaround: bool
        sleep-requests: bool
        sleep-interval: int
        sleep-interval: int
        sleep-subtitles: int

    Verbosity:
        quiet: bool
        no_warnings: bool

    Filesystem:
        output (outtmpl): str
    """
    def __init__(self, config: dict = None):
        self.dl_ops = {
            'outtmpl': join(expanduser("~/OneDrive/Desktop"), '%(title)s-%(id)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'throttled-rate': '100K'
        }
        self.ydl = yt_dlp.YoutubeDL(self.dl_ops)
        self.progress_callback = None
        self.emit_bool = None
        self.batch_count = 0
        self.batch_start = 0
        self.batch_number = 1

    def _set_dl_ops(self, dl_ops):
        for key in dl_ops:
            self.dl_ops[key] = dl_ops[key]

    def download_video(self, url, progress_callback=None):
        self.progress_callback = progress_callback
        self.emit_bool = True

        def my_hook(d):
            if self.emit_bool:
                if d['status'] == 'downloading' and self.progress_callback is not None:
                    self.progress_callback.emit(
                        round(
                            float(d['downloaded_bytes']) / float(d['total_bytes']) * 100,
                            1
                        )
                    )
            if d['status'] == 'finished':
                self.emit_bool = False

        self._set_dl_ops(
            {
                'noplaylist': True,
                'progress_hooks': [my_hook]
            }
        )
        self.ydl = yt_dlp.YoutubeDL(self.dl_ops)
        self.ydl.download([url])

    def download_playlist(self, url, progress_callback=None):
        self.progress_callback = progress_callback
        self.emit_bool = True
        def my_hook(d):
            if self.emit_bool:
                if d['status'] == 'downloading' and self.progress_callback is not None:
                    self.progress_callback.emit(
                        self.batch_start + round(
                            float(d['downloaded_bytes']) / float(d['total_bytes']) * 100 / self.batch_count * 0.5,
                            1
                        )
                    )
            if d['status'] == 'finished' and self.batch_count != 0:
                self.batch_start += 100 / self.batch_count * 0.5
                self.batch_number += 1
            if d['status'] == 'finished' and self.batch_number % 2 == 0:
                self.emit_bool = False
            if d['status'] == 'finished' and self.batch_number % 2 != 0:
                self.emit_bool = True

        self._set_dl_ops(
            {
                'noplaylist': False,
                'progress_hooks': [my_hook]
            }
        )
        if self.check_if_url_is_playlist(url):
            self.batch_count = self.get_number_of_videos_in_playlist(url)
            self.ydl = yt_dlp.YoutubeDL(self.dl_ops)
            self.ydl.download([url])

    def get_number_of_videos_in_playlist(self, url):
        return len(self.ydl.extract_info(url, download=False).get('entries'))

    def check_if_url_is_playlist(self, url):
        return self.ydl.extract_info(url, download=False).get('entries') is not None

    def update_dl_ops(self, key: str, value: str):
        if key == "download_location":
            key = "outtmpl"
            value = join(expanduser(value), '%(title)s-%(id)s.%(ext)s')
        if key == "file_pattern":
            key = "outtmpl"
            value = join(self.dl_ops["outtmpl"].split("%")[0], value)
        print(f"Updating {key} to {value}")
        self.dl_ops[key] = value
