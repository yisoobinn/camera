from PyQt5.QtCore import *
from PyQt5 import uic 
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys 
import matplotlib.pyplot as plt 
import numpy as np 
import cv2
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas



class data_test(QMainWindow):
    def __init__(self):
        super(data_test, self).__init__()
        uic.loadUi("test_data.ui", self)
        self.show()
        self.pButton.clicked.connect(self.start)
        self.input.clicked.connect(self.text1)
        self.text2 = ""
        #self.line_edit = input_text(self)
        
        
    def text1(self):
        self.text2 = self.input_text.text()
        self.input_text.setText(self.text2)
        #print(self.text2)

    def start(self):
        print(self.text2)
        
        # 시간 배열 생성
        time = np.linspace(0, float(self.text2)*np.pi, 100)
        # sin 파형 생성
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
window = data_test()
window.show()
sys.exit(app.exec_())
