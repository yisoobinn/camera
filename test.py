from PyQt5.QtCore import *
from PyQt5 import uic 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys 
import cv2 
import numpy as np 

class test_thread(QThread):
    def __init__(self, label):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.label = label

    def run(self):
        while True:
            ret, self.frame = self.cap.read()
            self.frame = cv2.resize(self.frame, (640,480))
            h, w, ch = self.frame.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(self.frame.data, w, h, bytes_per_line, QImage.Format_BGR888)
            qpixmap = QPixmap.fromImage(convert_to_Qt_format)
            self.label.setPixmap(qpixmap)
            self.label.show()



class test(QMainWindow):
    def __init__(self):
        super(test, self).__init__()
        uic.loadUi("test.ui", self)
        self.show()
        self.pButton.clicked.connect(self.Vision)
        
    def Vision(self):
        self.t = test_thread(self.label)
        self.t.start()


app = QApplication(sys.argv)
window = test()
window.show()
sys.exit(app.exec_())
