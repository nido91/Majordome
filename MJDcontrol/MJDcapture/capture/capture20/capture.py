import time
import picamera
from datetime import datetime, timedelta

# Take 10 photos
		
with picamera.PiCamera() as camera:
    camera.resolution = (1024, 768)
    time.sleep(0.5)
    i=0
    for capture in camera.capture_continuous('img{timestamp:%Y-%m-%d-%H-%M-%S}.jpg'):
#        print('Captured %s' % capture)
        time.sleep(0.5) # wait x sec
        i=i+1
        if i==10:
            break
		
