import cv2
import time
import numpy as np
import math
import Hand_Tracking_Module as htm
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
#pycaw python library allows us to change the volume of our computer
wCam, hCam= 640,480
cap=cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector=htm.handDetector(detectionCon=0.7)  #increase detection confidence bec that will give confidence that its a hand and will not flicker much.
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)
# volume.GetMute()
# volume.GetMasterVolumeLevel()
# print(volume.GetVolumeRange())  #first 2 values give volume range(-63.5 to 0)
volRange=volume.GetVolumeRange()
minVol=volRange[0]
maxVol=volRange[1]

pTime=0
while True:
    success,img=cap.read()
    img=detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList)!=0 :
    #  print(lmList[4],lmList[8])  # thumb and index finger coordinates
     x1,y1=lmList[4][1],lmList[4][2]  #thumb
     x2,y2=lmList[8][1],lmList[8][2]  #index
     cx,cy=(x1+x2)//2,(y1+y2)//2
     length=math.hypot(x1-x2,y1-y2)
     cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)
     cv2.circle(img,(x2,y2),10,(255,0,255),cv2.FILLED)
     cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)
     cv2.line(img,(x1,y1),(x2,y2),(255,0,255),2)
     #Hand Range: 25 to 250
     #vol range: -63.5 to 0  We must convert hand range to vol range. We have a fun for that !
     vol=np.interp(length,[25,250],[minVol,maxVol])#initial range & final range
     volume.SetMasterVolumeLevel(vol, None)
    #  print(int(length),int(vol))
     if length<20:
        cv2.circle(img,(cx,cy),10,(0,255,0),cv2.FILLED)
    cTime=time.time()
    fps=1/(cTime-pTime)
    pTime=cTime
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_PLAIN, 2,
                (255, 0, 0), 3)
    cv2.imshow('Frame',img)
    if cv2.waitKey(1) & 0xFF == ord('d'):
        break