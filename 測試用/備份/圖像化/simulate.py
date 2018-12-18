import sys
import os
import ntplib
import time
import source
import _thread
from datetime import datetime
print('initial...')
helpX=0
helpY=0
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

sensor1=source.sensor('sensor1',source.now(),source.generateTemp())
sensor2=source.sensor('sensor2',source.now(),source.generateTemp())
sensor3=source.sensor('sensor3',source.now(),source.generateTemp())
agg1=source.aggregator('agg1')
agg2=source.aggregator('agg2')
car1=car('car1')
map=source.map(9,9)
map.putCar(car1)
car1.printPosition()
sensor1.printState()
sensor2.printState()
sensor3.printState()
print('initial finished')

try:
    _thread.start_new_thread( source.autoSensor, (sensor1, ) )
    _thread.start_new_thread( source.autoSensor, (sensor2, ) )
    _thread.start_new_thread( source.autoSensor, (sensor3, ) )
    _thread.start_new_thread( car1.autoRun ,(map,) )
except:
    print('多工失敗')
time.sleep(1)

source.link(sensor1,agg1)
source.link(sensor2,agg1)
source.link(sensor3,agg2)
print('6666666666666')
while 1:
    print('----------------------------------------------')
    if sensor1.temperature>28:
        helpX=270+9*40
        helpY=130+6*40
        if car1.x==helpX and car1.y==helpY:
            source.link(sensor1,car1)
            print('car is near to sensor')
        else:
            print('car is going to help sensor')
    elif sensor1.temperature<28:
        helpX=0
        helpY=0
    
    if  helpX==0 or helpY==0:
        source.link(sensor1,agg1)
        print('it is out of crisis')
    time.sleep(2)


