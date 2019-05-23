import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import moviepy.editor as mpe
from scipy import misc
import cv2
import numpy as np

my_clip = mpe.VideoFileClip("output.mkv")
FPS = 60.0
white = (255, 255, 255)
width = 1280
height = 720
beep_length = 0.01
silence_length = 0.99
sample_rate = 44100
seconds = 10.0
samples = sample_rate * seconds

# this really depends on the compression
# by trial and error, it's at least 92% white
THRESHOLD = 0.92


def RGB2Int(value):
    value = list(value)
    value.reverse()
    return (value[0] << 16) + (value[1] << 8) + value[2]


int_white = RGB2Int(white)
int_threshold = int_white * THRESHOLD


def almost_white(color):
    int_color = RGB2Int(color)
    return int_color >= int_threshold


def assert_frame(i, first, frame):
    # we want to verify we have the white square
    # we try on spot, one pixel down, on pixel right
    y, x = divmod(i-first, width)
    info = "frame %d %s" % (i, str(frame[y + 1][x]))
    attempts = [
        (y, x),
        (y + 1, x),
        (y, x + 1),
        (y + 1, x + 1),
        (y, x - 1),
        (y - 1, x - 1),
    ]
    for wy, wx in attempts:
        ok = almost_white(frame[wy, wx])
        if ok:
            break
    if not ok:
        cv2.line(frame, (x - 1, y + 2), (x + 1, y + 2), (255, 0, 0), 1)
        cv2.line(frame, (x - 1, y), (x - 1, y + 2), (255, 0, 0), 1)
        cv2.line(frame, (x + 2, y), (x + 2, y + 2), (255, 0, 0), 1)
        misc.imsave("frame%d.png" % (i-first), frame)
        print("frame %d failed " % (i-first))


def assert_audio(i, frame):
    one_second, frames_in_sec = divmod(i, sample_rate)
    frames_with_sound = beep_length * sample_rate - 150
    if frames_in_sec <= frames_with_sound:
        assert all(frame != [0.0, 0.0]), "%i %s" % (i, str(frame))
    elif frames_in_sec <= frames_with_sound + 150:
        pass
    else:
        assert frame[0] < 0.011 and frame[1] < 0.011, frame


def find_viewport(frame):
    ret, thresh = cv2.threshold(frame, 230, 255, 0)
    gray = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(gray, 1, 2)
    bottom_x = bottom_y = top_x = top_y = 0
    for x, cnt in enumerate(contours):
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        if len(approx) == 4:
            x_, y_, w_, h_ = cv2.boundingRect(approx)
            if w_ > 200:
                return frame


print("Checking video 🎥")
first_frame = -1
for i, frame in enumerate(my_clip.iter_frames()):
    frame = frame[192:192+1292, 140:140+2296]
    frame = cv2.resize(frame, (1280, 720))
    cropped_frame = find_viewport(frame)
    if cropped_frame is None:
        print("viewport not found")
        continue
    if first_frame == -1:
        print("Found first image of browser viewport at %d" % i)
        cv2.imwrite("firstframe.png", cropped_frame)
        first_frame = i
    assert_frame(i, first_frame, cropped_frame)

print("Checking audio 🔊")
for i, frame in enumerate(my_clip.audio.iter_frames()):
    if i >= 44100:
        continue  # why do we have more?
    assert_audio(i, frame)

print("PASS 👌")
