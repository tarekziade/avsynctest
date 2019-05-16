import moviepy.editor as mpe

my_clip = mpe.VideoFileClip("noise.mp4")

FPS = 24

def RGB2Int(value):
    value = list(value)
    value.reverse()
    return (value[0] << 16) + (value[1] << 8) + value[2]

def assert_frame(i, frame):
    # we want to verify the color of the first point
    color = frame[0][0]
    int_color = RGB2Int(color)
    print("found:%d, frame: %d" % (int_color, i))

for i, frame in enumerate(my_clip.iter_frames()):
    assert_frame(i, frame)

