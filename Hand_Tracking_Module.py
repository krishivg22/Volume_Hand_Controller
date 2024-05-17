#! C:\Users\hp\Desktop\OpenCV\myenv\Scripts\python.exe
import cv2  
import mediapipe as mp
import time
import math
#Hand tracking-  Palm detection(Palm crop) + Hand landmark(21 points)                  


class handDetector():
    def __init__(self, mode=False, maxHands=2,model_complexity=1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.model_complexity=model_complexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.model_complexity,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds=[4,8,12,16,20]


    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findPosition(self, img, handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        self.lmList = []   #Now it can be used in other functions
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)  #landmark values in pixel
                xList.append(cx)
                yList.append(cy)
                # print(id, cx, cy)
                self.lmList.append([id, cx, cy])
                if draw:
            
                     cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
            xmin, xmax = min(xList), max(xList)
            ymin, ymax = min(yList), max(yList)
            bbox = xmin, ymin, xmax, ymax
            if draw:
               cv2.rectangle(img, (xmin - 20, ymin - 20), (xmax + 20, ymax + 20),  #ye direct original image me change la de rha h
               (0, 255, 0), 2)
        return self.lmList, bbox
       
    def fingersUp(self):
     fingers = []
     # Thumb
     if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]: #4 point(thumb) is right than 3 point.
         fingers.append(1)   #then thumb open
     else:
         fingers.append(0)  #closed
 
     # Fingers
     for id in range(1, 5):
         if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]: #ex: for index, 8 point is above 6, so open
             fingers.append(1)   #open
         else:
             fingers.append(0)   #closed
 
         # totalFingers = fingers.count(1)
 
     return fingers
    
    def findDistance(self, p1, p2, img, draw=True,r=15, t=3):  #p1,p2 are 2 landmark points, r->radius, t->thickness
     x1, y1 = self.lmList[p1][1:]
     x2, y2 = self.lmList[p2][1:]
     cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
 
     if draw:
         cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
         cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
         cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
         cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
         length = math.hypot(x2 - x1, y2 - y1)
 
     return length, img, [x1, y1, x2, y2, cx, cy]   #2 point coordinates and centre coordinates
     
#Now we can use this module directly in any project.

def main():
   cap = cv2.VideoCapture(0)
   pTime=cTime=0
   detector=handDetector()
   while True:
    success, img = cap.read()
    img=detector.findHands(img)
    lmlist=detector.findPosition(img)   #if we put draw=False, then it will not draw the points
    if len(lmlist)!=0 :
        print(lmlist[4])     #tip of thumb ke landmark coordinates de dega
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 255), 3)
    cv2.imshow('Frame',img)
    if cv2.waitKey(1) & 0xFF==ord('d'):             #cv.waitKey(20), it waits for each frame for 20 ms. If a key is pressed within that time, it returns the ASCII code of the key. If no key is pressed within 20 milliseconds, it returns -1.
     break



if __name__ == "__main__":
    main()