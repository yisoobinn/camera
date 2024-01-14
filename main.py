from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import sys 
import cv2 
import numpy as np 

class test_thread(QThread):
    def __init__(self, v1):
        super().__init__()
        self.v1 = v1
        self.cap = cv2.VideoCapture(0)
        self.net = cv2.dnn.readNet("yolov2-tiny.weights", "yolov2-tiny.cfg")
        self.classes = []
        with open("coco.names", "r") as f:
            self.classes =  [line.strip() for line in f.readlines()]
        self.layer_names = self.net.getLayerNames()

        self.output_layers = [self.layer_names[i - 1] for i in self.net.getUnconnectedOutLayers()]

        self.colors = np.random.uniform(0, 255, size=(len(self.classes), 3))

    def run(self):
        while True:
            ret,self.frame = self.cap.read() 
            img = cv2.resize(self.frame, None, fx=0.4, fy=0.4)
            height, width, channels = img.shape

            blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
            self.net.setInput(blob)
            outs = self.net.forward(self.output_layers)

            class_ids = []
            confidences = []
            boxes = []
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]

                    if confidence > 0.5:
                        center_x = int(detection[0] * width)
                        center_y = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)
                        boxes.append([x, y, w, h])
                        confidences.append(float(confidence))
                        class_ids.append(class_id)
            indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

            font = cv2.FONT_HERSHEY_TRIPLEX

            for i in range(len(boxes)):
                if i in indexes:
                    x, y, w, h = boxes[i]
                    label = str(self.classes[class_ids[i]])
                    color = self.colors[i]
                    cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
                    cv2.putText(img, label, (x, y-5), font, 0.5, color, 1)


            self.frame = cv2.resize(self.frame, (640, 480))
            h, w, ch = self.frame.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(self.frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            qpixmap = QPixmap.fromImage(convert_to_Qt_format)
            self.v1.setPixmap(qpixmap)
            self.v1.show()

class test2(QDialog):
    def __init__(self):
        super(test2,self).__init__()
        uic.loadUi("v.ui", self)
        self.show()
        self.s = test_thread(self.v)
        self.s.start()

class test1(QDialog):
    def __init__(self):
        super(test1, self).__init__()
        uic.loadUi("blue.ui", self)
        self.show()

class test(QMainWindow):
    def __init__(self):
        super(test, self).__init__()
        uic.loadUi("main.ui", self)
        self.show()

        self.pButton.clicked.connect(self.pop)
        self.Close.clicked.connect(self.Close1)
        self.pVision.clicked.connect(self.Vision)

    def pop(self):
        self.t = test1()

    def Close1(self):
        self.close()

    def Vision(self):
        self.v = test2()


app = QApplication(sys.argv)
window = test() 
window.show()
sys.exit(app.exec_())