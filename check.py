import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import moviepy.editor as mpe
from scipy import misc
import cv2

my_clip = mpe.VideoFileClip("noise.mp4")
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


def assert_frame(i, frame):
    # we want to verify we have the white square
    # we try on spot, one pixel down, on pixel right
    y, x = divmod(i, width)
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
        misc.imsave("frame%d.png" % i, frame)
    assert ok, "frame%d.png" % i


def assert_audio(i, frame):
    one_second, frames_in_sec = divmod(i, sample_rate)
    frames_with_sound = beep_length * sample_rate - 150
    if frames_in_sec <= frames_with_sound:
        assert all(frame != [0.0, 0.0]), "%i %s" % (i, str(frame))
    elif frames_in_sec <= frames_with_sound + 150:
        pass
    else:
        assert frame[0] < 0.011 and frame[1] < 0.011, frame


print("Checking video 🎥")
for i, frame in enumerate(my_clip.iter_frames()):
    ret, thresh = cv2.threshold(frame, 220, 255, 0)
    gray = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("tresh.png", gray)
    contours, hierarchy = cv2.findContours(gray, 1, 2)
    selected = []
    bottom_x = bottom_y = top_x = top_y = 0
    for x, cnt in enumerate(contours):
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        if len(approx) == 4:
            (x_, y_), (width_, height_), angle = cv2.minAreaRect(cnt)
            if height_ > 100:
                bottom_x = approx[0][0][0] + 1
                bottom_y = approx[-1][-1][-1] + 1
                #cv2.drawContours(frame,[cnt],0,(0,0,255), -1)
                print("found the browser viewport")
    top_x = bottom_x - width
    top_y = bottom_y - height
    cropped_img = frame[top_y:bottom_y, top_x:bottom_x]
    #cv2.imwrite("frame-%d.png" % i, cropped_img)

    assert_frame(i, cropped_img)

print("Checking audio 🔊")
for i, frame in enumerate(my_clip.audio.iter_frames()):
    if i >= 441000:
        continue  # why do we have more?
    assert_audio(i, frame)

print("PASS 👌")
