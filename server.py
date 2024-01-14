from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic 
import sys 
import numpy as np 
import socket 
import matplotlib.pyplot as plt
import cv2
import time

class receiver(QThread):
    def __init__(self, sock, sin_wave):
        super().__init__()
        self.sock = sock
        self.sin_wave = sin_wave
        self.sock.listen(100)

    def fun(self, value):
        self.t.wait = value

    def run(self):
        while True:
            self.new_sock, addr = self.sock.accept()
            self.t = sender(self.new_sock, self.sin_wave)
            self.t.start()


class sender(QThread):
    user = pyqtSignal(int)
    def __init__(self, new_sock, sin_wave):
        super().__init__()
        self.new_sock = new_sock
        self.sin_wave = sin_wave
        self.wait = 1
        
    def run(self):
        while True:
            #print(self.wait)

            if self.wait == 1:
                pass

            else:
                self.wait = 1
                stringData = self.sin_wave.tostring()
                self.new_sock.send(stringData)
                self.user.emit(1)

class server(QMainWindow):
    def __init__(self):
        super(server, self).__init__()
        uic.loadUi("socket.ui", self)
        self.show()

        self.input.clicked.connect(self.number)
        self.ipButton.clicked.connect(self.ip_number)

    def number(self):
        self.value = self.input_text.text()
        print(self.value)

        time = np.linspace(0, float(self.value)*np.pi*2, 100)
        self.sin_wave = np.sin(time)
        plt.plot(self.sin_wave)
        plt.savefig("1.png")
        self.img = cv2.imread("1.png")
        h, w, ch = self.img.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(self.img.data, w, h, bytes_per_line, QImage.Format_RGB888)
        qpixmap = QPixmap.fromImage(convert_to_Qt_format)
        self.label.setPixmap(qpixmap)
        self.label.show()

    def ip_number(self):
        self.ip_value = self.input_ip.text()
        print(self.ip_value)
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip_value, 8080))
    
        print("waiting to connect from client")

        self.s = receiver(self.sock, self.sin_wave)
        self.s.start()
        time.sleep(10)
        self.s.t.user.connect(self.ff)

    @pyqtSlot(int)
    def ff(self, value):
        print("data 보내기172")
        if value == 0:
            self.s.fun(1) 
        elif value == 1:
            self.s.fun(0)


app = QApplication(sys.argv)
window = server()
window.show()
sys.exit(app.exec_())