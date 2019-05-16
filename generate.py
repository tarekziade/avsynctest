import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc
import cv2
from moviepy.editor import AudioClip
import moviepy.editor as mpe

width = 1280
height = 720
FPS = 24
seconds = 10

fourcc = VideoWriter_fourcc(*'MP42')
video = VideoWriter('./noise.avi', fourcc, float(FPS), (width, height))

white = (255, 255, 255)

for i in range(FPS*seconds):
    frame = np.random.randint(0, 1,
                              (height, width, 3),
                              dtype=np.uint8)
    cv2.putText(frame, "%d" % i, (200, 200), cv2.FONT_HERSHEY_PLAIN, 10.0,
            white, 3, cv2.LINE_AA)
    video.write(frame)
video.release()

A440 = 440

def make_frame(i):
    value = np.cos(np.pi * i * A440)
    return value

clip = AudioClip(make_frame, duration=seconds)
clip.fps = 44100
my_clip = mpe.VideoFileClip('./noise.avi')
final_clip = my_clip.set_audio(clip.copy())
final_clip.write_videofile("noise.mp4")
