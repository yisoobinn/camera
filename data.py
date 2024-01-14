from PyQt5.QtCore import *
from PyQt5 import uic 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys 
import matplotlib.pyplot as plt 
import numpy as np 
import cv2
import socket

class test2(QDialog):
    signal_input = pyqtSignal(str)

    def __init__(self):
        super(test2, self).__init__()
        uic.loadUi("test2.ui", self)
        self.show()
        self.input.clicked.connect(self.text)

    def text(self):
        self.value = self.input_text.text()
        self.signal_input.emit(self.value)
        self.close()

class test(QMainWindow):
    def __init__(self):
        super(test, self).__init__()
        uic.loadUi("test.ui", self)
        self.show()
        self.first = 1
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("172.30.1.86", 10001))
        self.sock.listen(1)
        print("waiting to connect from client")
        self.new_sock, addr = self.sock.accept()
        self.pButton.clicked.connect(self.popup)
        
    def popup(self):
        self.s = test2()
        self.s.signal_input.connect(self.text)
        

    @pyqtSlot(str)  
    def text(self, input_string):
        if self.first == 1:
            self.first = 0
            self.string = input_string
            print(self.string)
            time = np.linspace(0, float(self.string)*np.pi*2, 100)
            sin_wave = np.sin(time)
            self.new_sock.send(sin_wave)

            plt.plot(sin_wave)
            plt.savefig("1.png")
            self.img = cv2.imread("1.png")
            h, w, ch = self.img.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(self.img.data, w, h, bytes_per_line, QImage.Format_RGB888)
            qpixmap = QPixmap.fromImage(convert_to_Qt_format)
            self.label.setPixmap(qpixmap)
            self.label.show()
        else:
            plt.clf()
            self.string = input_string
            print(self.string)
            time = np.linspace(0, float(self.string)*np.pi*2, 100)
            sin_wave = np.sin(time)
            plt.plot(sin_wave)
            plt.savefig("1.png")
            self.img = cv2.imread("1.png")
            h, w, ch = self.img.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(self.img.data, w, h, bytes_per_line, QImage.Format_RGB888)
            qpixmap = QPixmap.fromImage(convert_to_Qt_format)
            self.label.setPixmap(qpixmap)
            self.label.show()
    
app = QApplication(sys.argv)
window = test()
window.show()
sys.exit(app.exec_())
