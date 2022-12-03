import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
from snake import Snake


cap = cv2.VideoCapture(1)
cap.set(3,1280)
cap.set(4,720)

detector = HandDetector(detectionCon=0.8, maxHands=1)

game = Snake()
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    hands, frame = detector.findHands(frame, flipType=False)

    if hands:
        lmList = hands[0]['lmList'] # Get LandmarkList from hand 1.
        pIndex = lmList[8][0:2] # find Point index of finger.
        frame = game.update(frame, pIndex)

        

    cv2.imshow('Snake game', frame)
    key = cv2.waitKey(1)
    if key == ord('r'):
        game.gameOver = False
        game.score = 0
        