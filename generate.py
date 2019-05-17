"""
    Video Generator

    Creates a video we can use in our tests.

    Based on moviepy and opencv (so ffmpeg underneath)
"""
import os
import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc
import cv2
import moviepy.editor as mpe
from scipy.io import wavfile


config = {
    "width": 1280,
    "height": 720,
    "FPS": 24,
    "seconds": 10,
    "sample_rate": 44100,
    "frequency": 440,
    "beep_length": 1,
    "silence_length": 4,
}

white = (255, 255, 255)
black = (0, 0, 0)


class VideoGenerator:
    def __init__(self, filename, config):
        self.fourcc = VideoWriter_fourcc(*"MP42")
        self.filename = filename
        self.conf = config
        self.sound_loops = int(
            config["seconds"] / (config["beep_length"] + config["silence_length"])
        )
        self.width = self.conf["width"]
        self.height = self.conf["height"]
        self.FPS = self.conf["FPS"]
        self.video = VideoWriter(
            filename + ".avi",
            self.fourcc,
            float(self.conf["FPS"]),
            (self.width, self.height),
        )

    def generate_frame(self, color):
        pixel = np.array(black, dtype=np.uint8)
        line = np.array([pixel for _ in range(self.width)])
        return np.array([line for _ in range(self.height)])

    def generate(self):
        print("generate video in %s" % self.filename)
        for i in range(self.FPS * self.conf["seconds"]):
            frame = self.generate_frame(i)
            cv2.putText(
                frame,
                "%d" % i,
                (200, 200),
                cv2.FONT_HERSHEY_PLAIN,
                10.0,
                white,
                3,
                cv2.LINE_AA,
            )
            y, x = divmod(i, self.width)
            cv2.rectangle(frame, (x, y), (x + 1, y + 1), white, 1)
            self.video.write(frame)
        self.video.release()
        self.generate_sound()
        self.merge_audio_video()
        os.remove(self.filename + ".avi")
        os.remove(self.filename + ".wav")

    def generate_sound(self):
        print("generate audio")
        beep_length = self.conf["beep_length"]
        silence_length = self.conf["silence_length"]
        sample_rate = self.conf["sample_rate"]
        t = np.linspace(0, beep_length, sample_rate * beep_length)
        beep = np.sin(self.conf["frequency"] * 2 * np.pi * t)
        silence = np.linspace(0, silence_length, sample_rate * silence_length) * 0
        sequence = np.concatenate([beep, silence] * self.sound_loops)
        wavfile.write(self.filename + ".wav", sample_rate, sequence)

    def merge_audio_video(self):
        print("merge video+audio")
        clip = mpe.VideoFileClip(self.filename + ".avi")
        final_clip = clip.set_audio(mpe.AudioFileClip(self.filename + ".wav"))
        final_clip.write_videofile(self.filename)


gen = VideoGenerator("noise.mp4", config)
gen.generate()
