import subprocess
import time
import os

from marionette_harness.marionette_test import MarionetteTestCase
from marionette_harness.runtests import cli


_CMD = ["ffmpeg",
        #"-loglevel",  "panic",
        "-y", "-f",  "avfoundation",
        "-framerate",  "60" , "-i",  '1', "-t", "15",
"-crf",  "0",  "-preset",  "ultrafast", "output.mkv"]

_CMD = ["ffmpeg", "-y", "-t", "15", "-f", "avfoundation",  "-i",  "1",
        "-crf", "0", "-rtbufsize", "10000k", "-c:v", "libx264", "-preset" , "ultrafast",
        "-framerate", "60",
        "output.mkv"]

_B = "/Users/tarek/Dev/gecko/mozilla-central-opt/objdir-osx/dist/Nightly.app/Contents/MacOS/firefox"
url = "file:///Users/tarek/Dev/github.com/avsynctest/noise.mp4"


class VideoTest(MarionetteTestCase):

    def setUp(self):
        MarionetteTestCase.setUp(self)
        self.marionette.set_pref("media.autoplay.default", 1)

    def test_capture(self):
        self.marionette.start_session()
        p = subprocess.Popen(_CMD, stdout=subprocess.PIPE)
        time.sleep(2.)
        self.marionette.set_window_rect(height=720, width=1280)
        self.marionette.navigate(url)
        time.sleep(20)
        p.terminate()
        self.marionette.delete_session()


if __name__ == '__main__':
    import sys
    sys.argv.extend(['test_avsync.py', '--binary', _B, '--app', 'fxdesktop'])
    cli()
