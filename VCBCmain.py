import cv2
import time
import HandTrackingModule as ht
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as bc


#640,1920
#480,1080
width=1920
height=1080

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW) #,cv2.CAP_DSHOW

cap.set(3, width ) #setting the width of the window
cap.set(4, height) #setting the Height of the window
cap.set(10,100) #setting the image clarity 

detector = ht.handDetector(detectionCon=0.7)
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# volume.GetMute()
v1=volume.GetMasterVolumeLevel()
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
brightness=0
while True:
    success, img = cap.read()
    img = detector.findHands(img)
    ####
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        #print(lmList[8])
        x2, y2 = lmList[8][1], lmList[8][2]
        cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED)
        vol = np.interp(x2, [200, 1200], [maxVol, minVol])
        volume.SetMasterVolumeLevel(vol, None)
        brightness = np.interp(y2, [35, 350], [0, 100])
        bc.set_brightness(int(brightness))	    
    ###
    cv2.imshow("Image", img)
    if cv2.waitKey(1) ==ord('e'):
    	break