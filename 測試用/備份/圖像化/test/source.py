import sys
import os
import ntplib
import time
import random
import _thread
from datetime import datetime

class sensor():
    def __init__(self, ID, time, temp, dst=0):
        self.ID=ID
        self.time=time
        self.temperature=temp
        self.dst=dst
    def printState(self):
        if self.dst==0:
            return 'ID='+self.ID+', time='+self.time+', temperature='+str(self.temperature)+', do not have any dst'
        else:
            return 'ID='+self.ID+', time='+self.time+', temperature='+str(self.temperature)+', dst='+self.dst
def now():
    ans = datetime.now()
    ans = str(ans.hour) + ":" + str(ans.minute) + ":" + str(ans.second)
    return ans

def generateTemp(temp=25):
    return temp

class car():
    def __init__(self, ID, x=0, y=0):
        self.ID=ID
        self.x=x
        self.y=y
    def moveUp(self):
        self.y=self.y-40
        return self.y
    def moveDown(self):
        self.y=self.y+40
        return self.y
    def moveLeft(self):
        self.x=self.x-40
        return self.x
    def moveRight(self):
        self.x=self.x+40
        return self.x
    def printPosition(self):
        print('car is at ({:d},{:d})'.format(self.x,self.y))
    def autoRun(self,map):
        while 1:
            global helpX
            global helpY
            if self.x==helpX and self.y==helpY:
                print('is helping sensor')
            elif self.x!=helpX or self.x!=helpY:
                print('helpX=',helpX)
                if self.x==270 and self.y-130<map.tate:
                    self.moveDown()
                elif self.x>=270 and self.x-270<map.yoko and self.y-130==map.tate:
                    self.moveRight()
                elif self.x-270==map.yoko and self.y>130:
                    self.moveUp()
                elif self.x-270<=map.yoko and self.y-130==0:
                    self.moveLeft()
            self.printPosition()
            time.sleep(0.2)
        
class map():
    def __init__(self, yoko, tate):
        self.yoko=yoko
        self.tate=tate
    def putCar(self,car,x=0,y=0):
        car.x=x
        car.y=y

class aggregator():
    def __init__(self, ID, x=0, y=0):
        self.ID=ID
        self.x=x
        self.y=y
def link(sensor,dst):
    sensor.dst=dst.ID
def autoSensor(sensor):
    sensor.time=now()
    temp=25
    if int(datetime.now().second)>30:
        temp=30
    sensor.temperature=generateTemp(temp)
    #sensor.printState()

    
        
