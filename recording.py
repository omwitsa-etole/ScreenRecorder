import cv2
import numpy as np
import sys
import pyautogui
from PySide6.QtGui import *
from PySide6 import *
from PIL.ImageQt import ImageQt
from PIL import Image

class Record():
	def __init__(self,output,obj):
		self.label = obj
		self.output = output
		SCREEN_SIZE = tuple(pyautogui.size())
		resolution = (1200, 800)
		#fourcc = cv2.VideoWriter_fourcc(*'MP4V')
		#self.out = cv2.VideoWriter(output, fourcc, 20.0, (SCREEN_SIZE))
		self.run()
	def run(self):
		webcam = cv2.VideoCapture()
		while True:
			img = pyautogui.screenshot()
			#img = np.array(img)
			#img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
			self.write(img)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				self.stop()
				break
	def kill(self):
		self.stop()
	def stop(self):
		#self.out.release()
		cv2.destroyAllWindows()
	def write(self,img):
		qim = ImageQt(img)
		pix = QPixmap.fromImage(qim)
		self.label.setPixmap(pix)
		self.label.setText("new file")
if __name__=="__main__":
	if len(sys.argv) > 1:
		r = Record(sys.argv[1])
		r.run()
