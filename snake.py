import numpy as np
import math
import cv2
import random
import cvzone

pathFood = 'donut.png'


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
        self.score = 0
        self.gameOver = False

    def randomFoodLocate(self):
        self.foodPoint = random.randint(100,1000), random.randint(100,600)


    def update(self, frame, currentHead) :
        
        if self.gameOver:
            cvzone.putTextRect(frame, 'Game Over', [300,400], scale=7, thickness=5, offset=20)
            cvzone.putTextRect(frame, f'Your score is {self.score}', [300,550], scale=7, thickness=5, offset=20)
            

        else : 

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

            #Check if snake eat food
            rx, ry = self.foodPoint
            if rx <= cx <= rx + 60 and ry <= cy <= cy+60 :
                self.score += 1
                self.randomFoodLocate()
                self.allowLength += 100

            #Drawing snake
            if self.point:
                for i, p in enumerate(self.point):
                    if i != 0:
                        cv2.line(frame, self.point[i-1], self.point[i], (0,0,255), 20)
                cv2.circle(frame, self.point[-1], 20, (200,0,200), cv2.FILLED)

            #Drawing food
            rx, ry = self.foodPoint
            # frame = cvzone.overlayPNG(frame, self.imgFood, (rx - self.wFood // 2 , ry - self.hFood // 2) )
            cv2.circle(frame, (rx, ry), 30, (255,0,0), cv2.FILLED)
            cvzone.putTextRect(frame, f'Score : {self.score}', [50,80], scale=3, thickness=3, offset=10)

            #Check for colinson
            pts = np.array(self.point[:-2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], False, (0,200, 0), 3)
            minDist = cv2.pointPolygonTest(pts, (cx,cy), True)

            if -1 <= minDist <= 1:  # When snake hit self
                print('Hit')
                self.gameOver = True

                # Reset all properties
                self.point = [] #Point of snake
                self.lengths = [] #Distance between point
                self.currentLength = 0
                self.allowLength = 200 # when eat food allowlength will increase
                self.previousHead = 0, 0 
                self.randomFoodLocate()



        
            
        return frame

                
