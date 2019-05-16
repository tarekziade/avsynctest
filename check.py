import moviepy.editor as mpe

my_clip = mpe.VideoFileClip("noise.mp4")

FPS = 24.0
white = (255, 255, 255)
width = 1280
height = 720


def almost_white(color):
    int_color = RGB2Int(color)
    int_white = RGB2Int(white)
    delta = abs(int_white - int_color)
    return delta < 256 * 256 * 256 * 0.06


def RGB2Int(value):
    value = list(value)
    value.reverse()
    return (value[0] << 16) + (value[1] << 8) + value[2]


def assert_frame(i, frame):

    # we want to verify we have the white square
    y, x = divmod(i, width)
    info = "frame %d %s" % (i, str(frame[y][x]))
    assert almost_white(frame[y][x]), info


for i, frame in enumerate(my_clip.iter_frames()):
    assert_frame(i, frame)
