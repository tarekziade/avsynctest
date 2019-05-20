import moviepy.editor as mpe
from scipy import misc
import cv2

my_clip = mpe.VideoFileClip("noise.mp4")

FPS = 24.0
white = (255, 255, 255)
width = 1280
height = 720

# this really depends on the compression
THRESHOLD = 0.07

def almost_white(color):
    int_color = RGB2Int(color)
    int_white = RGB2Int(white)
    delta = abs(int_white - int_color)
    return delta < 255 * 255 * 255 * THRESHOLD

def RGB2Int(value):
    value = list(value)
    value.reverse()
    return (value[0] << 16) + (value[1] << 8) + value[2]

def assert_frame(i, frame):
    # we want to verify we have the white square
    # we try on spot, one pixel down, on pixel right
    y, x = divmod(i, width)
    info = "frame %d %s" % (i, str(frame[y + 1][x]))
    print(info)
    attempts = [(y, x), (y + 1, x), (y, x +1), (y + 1, x + 1),
                (y, x - 1), (y - 1, x - 1)]
    for wy, wx in attempts:
        ok = almost_white(frame[wy, wx])
        if ok:
            break
    if not ok:
        cv2.line(frame, (x - 1, y + 2), (x + 1 , y + 2),(255,0,0), 1)
        cv2.line(frame, (x - 1, y), (x - 1 , y + 2),(255,0,0), 1)
        cv2.line(frame, (x + 2, y), (x + 2 , y + 2),(255,0,0), 1)
        misc.imsave("frame%d.png" % i, frame)
    assert ok, "frame%d.png" % i


for i, frame in enumerate(my_clip.iter_frames()):
    assert_frame(i, frame)
