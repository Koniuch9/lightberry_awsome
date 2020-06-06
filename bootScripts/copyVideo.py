import os

os.system("sudo modprobe v4l2loopback devices=2")
os.system("ffmpeg -f video4linux2 -i /dev/video0 -codec copy -f v4l2 /dev/video2 -codec copy -f v4l2 /dev/video3")
