import numpy as np
from cv2 import VideoWriter, VideoWriter_fourcc
import cv2
from moviepy.editor import AudioClip
import moviepy.editor as mpe


width = 1280
height = 720
FPS = 24
seconds = 10

fourcc = VideoWriter_fourcc(*"MP42")
video = VideoWriter("./noise.avi", fourcc, float(FPS), (width, height))

white = (255, 255, 255)

# todo, distribute value in the 3 colors instead of incrementing
# red first
def Int2RGB(value):
    return (value >> 16) & 255, (value >> 8) & 255, value & 255

def RGB2Int(value):
    return value[0] << 16 + value[1] << 8 + value[2]

def generate_frame(color):
    pixel = np.array(Int2RGB(color), dtype=np.uint8)
    print(Int2RGB(color), color)
    line = np.array([pixel for _ in range(width)])
    return np.array([line for _ in range(height)])


for i in range(FPS * seconds):
    frame = generate_frame(i)
    cv2.putText(
        frame, "%d" % i, (200, 200), cv2.FONT_HERSHEY_PLAIN, 10.0, white, 3, cv2.LINE_AA
    )
    video.write(frame)
video.release()

A440 = 440


def make_frame(i):
    value = np.cos(np.pi * i * A440)
    return value


clip = AudioClip(make_frame, duration=seconds)
clip.fps = 44100
my_clip = mpe.VideoFileClip("./noise.avi")
final_clip = my_clip.set_audio(clip.copy())
final_clip.write_videofile("noise.mp4")

