# coding:utf-8
from PyQt5 import QtGui,QtWidgets,QtCore
import sys
 
class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
 
    def init_ui(self):
        self.setWindowTitle("動畫使用-zmister.com") # 設置窗口標題
        self.resize(400,200) # 規定窗口大小
        self.main_widget = QtWidgets.QWidget() # 創建一個widget部件
        self.button = QtWidgets.QPushButton('射門',self.main_widget) # 創建一個按鈕
        self.button.setGeometry(10,10,60,30) # 設置按鈕位置
        self.button.clicked.connect(self.shoot)
        self.label = QtWidgets.QLabel(self.main_widget) # 創建一個文本標籤部件用於顯示足球
        self.label.setGeometry(50,80,50,50) # 設置足球位置
        png = QtGui.QPixmap()  # 創建一個繪圖類
        png.load("car.png")  # 從png中加載一個圖片
        self.label.setPixmap(png)  # 設置文本標籤的圖形
        self.label.setScaledContents(True) # 圖片隨文本部件的大小變動
 
        self.qiumen = QtWidgets.QLabel(self.main_widget)  # 創建一個文本標籤部件用於顯示球門
        self.qiumen.setGeometry(345, 75, 50, 50)  # 設置球門位置
        pngqiumen = QtGui.QPixmap()  # 創建一個繪圖類
        pngqiumen.load("fire.png")  # 從png中加載一個圖片
        self.qiumen.setPixmap(pngqiumen)  # 設置文本標籤的圖形
 
        self.setCentralWidget(self.main_widget)
 
    def shoot(self):
        self.anim = QtCore.QPropertyAnimation(self.label,b'geometry') # 設置動畫的對象及其屬性
        self.anim.setDuration(2000) # 設置動畫間隔時間
        self.anim.setStartValue(QtCore.QRect(50,80,50,50)) # 設置動畫對象的起始屬性
        self.anim.setEndValue(QtCore.QRect(350, 80, 50, 50)) # 設置動畫對象的結束屬性
        self.anim.start() # 啟動動畫
 
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())
