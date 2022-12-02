import numpy as np
import math
import cv2
import random
import cvzone

pathFood = 'cup-cake.png'


class Snake:
    def __init__(self) -> None:

        self.point = [] #Point of snake
        self.lengths = [] #Distance between point
        self.currentLength = 0
        self.allowLength = 200 # when eat food allowlength will increase
        self.previousHead = 0, 0 

        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.hFood, self.wFood ,_ = self.imgFood.shape #width and height of food.
        self.foodPoint = 0, 0
        self.randomFoodLocate()

    def randomFoodLocate(self):
        self.foodPoint = random.randint(100,1000), random.randint(100,600)


    def update(self, frame, currentHead) :

        px, py = self.previousHead
        cx, cy = currentHead # Current head and previous head to calculete length that update/change

        self.point.append([cx, cy])
        distance = math.hypot(cx - px, cy - py)
        self.lengths.append(distance)
        self.currentLength += distance
        self.previousHead = cx, cy

        #Length reduce
        if self.currentLength > self.allowLength :
            for i, length in enumerate(self.lengths):
                self.currentLength -= length
                self.lengths.pop(i)
                self.point.pop(i)
                if self.currentLength <= self.allowLength:
                    break

        #Drawing snake
        if self.point:
            for i, p in enumerate(self.point):
                if i != 0:
                    cv2.line(frame, self.point[i-1], self.point[i], (0,0,255), 20)
            cv2.circle(frame, self.point[-1], 20, (200,0,200), cv2.FILLED)

        #Drawing food
        rx, ry = self.foodPoint
        frame = cvzone.overlayPNG(frame, self.imgFood, (rx , ry) )
            
        return frame

                
