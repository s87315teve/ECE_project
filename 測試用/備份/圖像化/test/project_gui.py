# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QApplication
from Ui_project_gui import Ui_Dialog
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QThread
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import source
import os
import ntplib
import time
import _thread
from datetime import datetime
helpX=0
helpY=0
car_message='WTF'
message_car=''
message_sensor=''
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

class MyThread_car(QThread):  
  
    signal = pyqtSignal(str) # 信号类型：str
    def __init__(self):  
        super().__init__()
  
    def run(self):  
        while 1:
            global message_car
            self.signal.emit(message_car)
            time.sleep(0.5)
class MyThread_sensor(QThread):  
  
    signal = pyqtSignal(str) # 信号类型：str
    def __init__(self):  
        super().__init__()
  
    def run(self):  
        while 1:
            global message_sensor
            self.signal.emit(message_sensor)
            time.sleep(1)

              

class Dialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        self.nowX=0
        self.nowY=0
        self.tempX=270
        self.tempY=130
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        thread_car = MyThread_car() # 创建一个线程 
        thread_car.signal.connect(self.update_car) # 线程发过来的信号挂接到槽：update
        self.pushButton_start.clicked.connect(lambda : thread_car.start())
        thread_sensor = MyThread_sensor() # 创建一个线程 
        thread_sensor.signal.connect(self.update_sensor) # 线程发过来的信号挂接到槽：update
        self.pushButton_start.clicked.connect(lambda : thread_sensor.start())
        

    def update_car(self):  
        self.textBrowser_car.setText(message_car)
    def update_sensor(self):  
        self.textBrowser_sensor.setText(message_sensor)
    @pyqtSlot()
    def autoRun(self,map, car):
        while 1:
            global helpX
            global helpY
            self.tempX=car.x
            self.tempY=car.y
            print('helpX=',helpX,',helpY= ',helpY)
            if car.x==helpX and car.y==helpY:
                print('666')
                #self.textBrowser_car.setText('到了')
                global message_car
                message_car='到了'
            elif car.x!=helpX or car.x!=helpY:
                if car.x==270 and car.y-130<map.tate:
                    car.moveDown()
                elif car.x>=270 and car.x-270<map.yoko and car.y-130==map.tate:
                    car.moveRight()
                elif car.x-270==map.yoko and car.y-130>0:
                    car.moveUp()
                elif car.x-270<=map.yoko and car.y-130==0:
                    car.moveLeft()
            self.nowX=car.x
            self.nowY=car.y
            if self.tempX!=self.nowX or self.tempY!=self.nowY:
                self.anim = QtCore.QPropertyAnimation(self.label_car1,b'geometry') # 設置動畫的對象及其屬性
                self.anim.setDuration(0) # 設置動畫間隔時間
                self.anim.setStartValue(QtCore.QRect(self.tempX, self.tempY, 21, 21)) # 設置動畫對象的起始屬性
                self.anim.setEndValue(QtCore.QRect(self.nowX, self.nowY, 21, 21)) # 設置動畫對象的結束屬性
                self.anim.start() # 啟動動畫
            car.printPosition()
            source.autoSensor(self.sensor1)
            source.autoSensor(self.sensor2)
            source.autoSensor(self.sensor3)
            global message_sensor
            message_sensor=self.sensor1.printState()+'\n'+self.sensor2.printState()+'\n'+self.sensor3.printState()
            if self.sensor1.temperature>28:
                helpX=270+9*40
                helpY=130+6*40
                if self.car1.x==helpX and self.car1.y==helpY:
                    source.link(self.sensor1,self.car1)
                    message_car='car is near to sensor'
                    print('car is near to sensor')
                else:
                    message_car='car is going to help sensor'
                    print('car is going to help sensor')
            elif self.sensor1.temperature<28:
                helpX=0
                helpY=0
            if  helpX==0 or helpY==0:
                source.link(self.sensor1,self.agg1)
                message_car='it is out of crisis'
                print('it is out of crisis')            
            QThread.msleep(500)
    
    """
    @pyqtSlot()
    def moveCar(self):
        self.anim = QtCore.QPropertyAnimation(self.label_car1,b'geometry') # 設置動畫的對象及其屬性
        self.anim.setDuration(0) # 設置動畫間隔時間
        self.anim.setStartValue(QtCore.QRect(self.tempX, self.tempY, 21, 21)) # 設置動畫對象的起始屬性
        self.anim.setEndValue(QtCore.QRect(self.nowX, self.nowY, 21, 21)) # 設置動畫對象的結束屬性
        self.anim.start() # 啟動動畫
        time.sleep(0.5)
    """

    @pyqtSlot()
    def on_pushButton_start_clicked(self):
        _thread.start_new_thread(self.autoRun ,(self.map,self.car1, ) )
        #thread_car = QtCore.QThread()
        #thread_car.started.connect(self.testrun())
        #QThread.create(self.autoRun, (self.map,self.car1,  ) )
        #_thread.start_new_thread(self.testrun ,( ) )
        #_thread.start_new_thread(self.moveCar ,( ) )
        #_thread.start_new_thread( source.autoSensor, (self.sensor1, ) )
        #_thread.start_new_thread( source.autoSensor, (self.sensor2, ) )
        #_thread.start_new_thread( source.autoSensor, (self.sensor3, ) )
        global car_message
        """
        while 1:
            self.textBrowser_car.setText(car_message)
            car_message=car_message+'a'
            time.sleep(1)

        global helpX
        global helpY
        if self.sensor1.temperature>28:
            helpX=270+9*40
            helpY=130+6*40
            if self.car1.x==helpX and self.car1.y==helpY:
                source.link(self.sensor1,self.car1)
                print('car is near to sensor')
            else:
                print('car is going to help sensor')
        elif self.sensor1.temperature<28:
            helpX=0
            helpY=0
        if  helpX==0 or helpY==0:
            source.link(self.sensor1,self.agg1)
            print('it is out of crisis')

        time.sleep(1)
        """
            
    @pyqtSlot()
    def on_pushButton_initial_clicked(self):
        print('PASS 1')
        self.img=QtGui.QPixmap('car.png')
        self.label_car1.setPixmap(self.img)
        self.img=QtGui.QPixmap('sensor.png')
        self.label_sensor1.setPixmap(self.img)
        self.label_sensor2.setPixmap(self.img)
        self.label_sensor3.setPixmap(self.img)
        self.img=QtGui.QPixmap('agg.png')
        self.label_agg1.setPixmap(self.img)
        self.label_agg2.setPixmap(self.img)
        self.label_car1.setScaledContents(True)
        self.label_sensor1.setScaledContents(True)
        self.label_sensor2.setScaledContents(True)
        self.label_sensor3.setScaledContents(True)
        self.label_agg1.setScaledContents(True)
        self.label_agg2.setScaledContents(True)
        self.sensor1=source.sensor('sensor1',source.now(),source.generateTemp())
        self.sensor2=source.sensor('sensor2',source.now(),source.generateTemp())
        self.sensor3=source.sensor('sensor3',source.now(),source.generateTemp())
        self.agg1=source.aggregator('agg1')
        self.agg2=source.aggregator('agg2')
        self.car1=car('car1')
        self.map=source.map(360,360)
        self.map.putCar(self.car1, 270, 130)
        source.link(self.sensor1,self.agg1)
        source.link(self.sensor2,self.agg1)
        source.link(self.sensor3,self.agg2)
        self.textBrowser_sensor.setText ('initial finished')
        self.textBrowser_car.setText ('initial finished')
        print('PASS 2')
        
if __name__ == "__main__":
   if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = Dialog()
    dlg.show()
    sys.exit(app.exec_())
    

