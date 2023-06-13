from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtWidgets import *
from PySide6 import *
from PySide6.QtWebEngineWidgets import * 
from PySide6.QtGui import QPixmap
from PySide6.QtCore import *
from recording import Record
import subprocess
import sys
import pyautogui
import time
from PIL.ImageQt import ImageQt

class Recorder():
	def __init__(self,parent,label,layout,button,log,out,r):
		#super().__init__()
		#print("in recorder")
		if "mp4" not in out:
			out+=".mp4"
		#self = parent
		self.output = label
		#print(vars(label))
		#self.setVideoOutput(self.output)
		
		"""
		if "null" in str(label.pixmap()):
			
			#layout.removeItem(layout.takeAt(0))
			
			#print(vars(layout))
			label.setPixmap(QPixmap("img/video_frame.png"))
			button.setText("Start Recording")
			#layout.removeItem(layout.takeAt(0))
			log.write("Stopped Recording")
		else:
			
			label.setPixmap(QPixmap())
			#layout.removeItem(layout.takeAt(0))
			label.setText("New Instance")
			button.setText("Stop Recording")
			log.write("STarted New Recording")
		"""
		#self.setSource(QUrl("recording/output.mp4"))
		print(r)
		
		if not layout.isEmpty():
			if r != None:
				r.stop()
				log.write("Recording stopped")
				button.setText("Start Recording")
			else:
				log.write("Saving output to",out)
				button.setText("Stop Recording")
				label.setAlignment(Qt.AlignCenter)
				label.setPixmap(QPixmap())
				#r =  subprocess.Popen(['python recording.py '+out], shell=True)
				#log.write(r.stdout)
				#if r.stderr:
					#log.write(r.stderr)
				log.write("Recording started")
				r = QTimer()
				r.setInterval(1000)
				r.timeout.connect(lambda:self.capture())
				r.start()
				print(r.isActive())			
				#r = Record(out,label)
				#self.setSource(QUrl(out))
				#self.play()
				
				
			#print("clearing",layout.isEmpty())
			#label.setPixmap(QPixmap())
			#layout.removeItem(layout.takeAt(0))
			
			#label.setText("New instance")
			#label.setAlignment(Qt.AlignCenter)
			
			#frame2_layout = QVBoxLayout()
			#self.widget.setLayout(frame2_layout)
			#layout.addWidget(label)
			#layout.removeItem(layout.takeAt(0))
		#parent = self.widget
		#self.widget.show()
	def capture(self):
		print(r)
		log.write("capturing---")
		#img = pyautogui.screenshot()
		#qim = ImageQt(img)
		#pix = QPixmap.fromImage(qim)
		#self.output.setPixmap(pix)
		log.write("captured---")
