from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic 
import sys 
import numpy as np 
import socket 

import matplotlib.pyplot as plt
import cv2

class receiver(QThread):

    def __init__(self, sock, label):
        super().__init__()
        self.sock = sock
        self.label = label
        self.first = 1 


    def run(self):
        while True:
            if self.first == 1:
                self.first = 0
                self.sin_wave = self.sock.recv(100)
                self.aa = np.fromstring(self.sin_wave, dtype='uint8')
                plt.plot(self.aa)
                plt.savefig("2.png")
                self.img = cv2.imread("2.png")
                h, w, ch = self.img.shape
                bytes_per_line = ch * w
                convert_to_Qt_format = QImage(self.img.data, w, h, bytes_per_line, QImage.Format_RGB888)
                qpixmap = QPixmap.fromImage(convert_to_Qt_format)
                self.label.setPixmap(qpixmap)
                self.label.show()

            elif self.first == 0:
                    
                plt.clf()
                self.sin_wave = self.sock.recv(100)
                print("recving")
                self.aa = np.fromstring(self.sin_wave, dtype='uint8')
                plt.plot(self.aa)
                plt.savefig("2.png")
                self.img = cv2.imread("2.png")
                h, w, ch = self.img.shape
                bytes_per_line = ch * w
                convert_to_Qt_format = QImage(self.img.data, w, h, bytes_per_line, QImage.Format_RGB888)
                qpixmap = QPixmap.fromImage(convert_to_Qt_format)
                self.label.setPixmap(qpixmap)
                self.label.show()



class sender(QThread):
    def __init__(self, new_sock, sin_wave):
        super().__init__()
        self.new_sock = new_sock
        self.sin_wave = sin_wave
        
    def run(self):
        while True:
            self.send(self.sin_wave)


class client(QMainWindow):
    def __init__(self):
        super(client, self).__init__()
        uic.loadUi("sock.ui", self)
        self.show()

        self.ipButton.clicked.connect(self.ip_number)

    def ip_number(self):
        self.ip_value = self.input_ip.text()
        print(self.ip_value)
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip_value, 8080))
    
        print("connected server")

        self.s = receiver(self.sock, self.label)
        self.s.start()


app = QApplication(sys.argv)
window = client()
window.show()
sys.exit(app.exec_())