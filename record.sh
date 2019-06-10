ffmpeg -y -f avfoundation -framerate 60 -video_size 1920x1080 -i "1:0" -vsync 0  -vcodec h264_videotoolbox -acodec mp2 -b:v 1M -b:a 192k output.mp4
