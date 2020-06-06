import numpy as np
import cv2
import time
import os

os.system("hyperion-v4l2 --pixel-format YUYV --screenshot --device /dev/video2")
cap = cv2.VideoCapture(3)
noSignal = None
hyperionStarted = False

while(True):
	time.sleep(1)
	ret, frame = cap.read()
	err = 10.0
	if noSignal is None:
		noSignal = cv2.imread('/home/pi/videoCapture/noSignal.jpg', 0)
	try:
		grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		err = np.sum((noSignal.astype('float') - grey.astype('float')) ** 2)
		err /= 153600.0
	except:
		pass
	if err < 20.0 and hyperionStarted:
		os.system('sudo service hyperion stop')
		hyperionStarted = False
	if err > 20.0 and not hyperionStarted:
		os.system('sudo service hyperion start')
		hyperionStarted = True

cap.release()
