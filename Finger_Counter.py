import cv2 
import time
import os
import Hand_Tracking_Module as htm

pastTime = 0
currentTime = 0

# Creating the video capture object using my laptops video camera
cap = cv2.VideoCapture(0)

# Setting the width and height of the camera display
camWidth, camHeight = 640*2, 360*2
cap.set(3,camWidth)
cap.set(4,camHeight)

detector = htm.handDetector(dCon=0.7, tCon=0.7)

tipId = [4, 8, 12, 16, 20]

while True:
    # Getting the video from the camera
    success, img = cap.read()

    # Using findHands function in the Hand_Tracking_Module to overlay hand mesh on hand in the image captured by the camera
    img = detector.findHands(img)
    lmList = detector.findPos(img,draw=False)

    if len(lmList) != 0:
        fingers = []

        # This if statement is pertaining to the thumb
        if lmList[tipId[0]][1] > lmList[tipId[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # This if statement is pertaining to the four fingers
        for id in range(1,5):
            if lmList[tipId[id]][2] < lmList[tipId[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        totalFingers = fingers.count(1)
        cv2.putText(img,f'Count:{int(totalFingers)}', (camWidth-240,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)


    # Getting timestamps to be able to use the trackers positioning data
    currentTime = time.time()
    framesPerSec = 1/(currentTime-pastTime)
    pastTime = currentTime
    # Displaying the frames per second the the screen
    cv2.putText(img,f'FPS:{int(framesPerSec)}', (40,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 3)

    # Showing the video from camera in a window
    cv2.imshow("Image",img)
    cv2.waitKey(1)