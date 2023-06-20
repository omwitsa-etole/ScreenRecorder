import sys
import os
from os import system,name
from PySide6.QtCore import Qt
import signal
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtWidgets import *
from PySide6 import *
from PySide6.QtWebEngineWidgets import * 
from PySide6.QtGui import *
from PySide6.QtMultimediaWidgets import *
#from recorder import Recorder
import random
from logger import OutLog
from PySide6.QtCore import *
import pyautogui
import time
from PIL.ImageQt import ImageQt
import cv2
import numpy as np
from help import Help

out_file = None
max_width = 630
max_height = 400
extension = ".mp4"
recording = None
out_dir = sys.path[0]
app = QtWidgets.QApplication(sys.argv)
timer = QTimer()
log = None
out = None
recents = []

def launch(app):
	global log
	def sigint_handler(*args):
		#LOGGER.info("Received SIGINT, exiting...")
		#main_window.on_exit()
		app.quit()
	signal.signal(signal.SIGINT, sigint_handler)
	widget = QWidget()

	menu = QMenuBar(widget)
	tool_menu = menu.addMenu('Home')
	#menu.addMenu("File")
	hlp = QAction("?")
	menu.addAction(hlp)
	edit_dir = QAction("Edit directory")
	exit_button = QAction('Exit')
	exit_button.setShortcut("Ctrl+Q")
	edit_dir.setShortcut("Ctrl+D")
	exit_button.triggered.connect(app.quit)	
	hlp.triggered.connect(lambda:Help(widget,log))
	tool_menu.addAction(exit_button)
	tool_menu.addAction(edit_dir)

	frame1 = QWidget()
	LOGGER = OutLog()#.setReadOnly(True)
	

	log = LOGGER
	log.write("Started app successfull")
	#log.setReadOnly(True)
	frame1_0 = QWidget()
	frame1_1 = QWidget()
	frame1_1_1 = LOGGER
	frame2 = QtMultimedia.QMediaPlayer()#sproutgl frame >> Edit this fram attribute for Sproutgl
	frame2_0 = QLabel()#QVideoWidget()#QLabel()
	frame2_0.setAlignment(Qt.AlignCenter)
	#LOGGER.append("STarted app")
	pixmap = QPixmap("img/video_frame.png")  
	#frame2_0.show()
	frame2_0.setPixmap(pixmap)

	#frame2.setSource(QUrl("recording/output.mp4"))

	#frame2.setAlignment()
	frame2_0.setStyleSheet("border: 1px solid white;border-radius: 4px;text-align:center;")
	#frame1_1_1.setStyleSheet("border: 1px solid white;border-radius: 4px;text-align:center;")
	frame1_1_1.setMinimumSize(max_height-130,max_height-150)
	frame2_0.setMinimumWidth(max_width)
	frame2_0.setMinimumHeight(max_height)
	frame1.setMaximumWidth(max_width/2)
	#slider = QScrollBar()
	#slider.setMaximum(125)

	frame1_1_layout = QHBoxLayout()
	frame1_1.setLayout(frame1_1_layout)

	frame1_0_layout = QFormLayout() 
	frame1_0.setLayout(frame1_0_layout)
	#frame1_1.setFixedWidth(180)

	save_as = QLineEdit()	
	save_as.insert(str(random.randint(0,1000001)))
	enable_audio = QCheckBox()
	start_record = QPushButton("Start Recording")
	play_record = QPushButton("Play Recording")
	new_dir = QPushButton(out_dir)
	output_dir = QLineEdit()
	output_dir.insert(out_dir)
	new_dir.setMaximumWidth(150)
	output_dir.setMaximumWidth(150)
	output_dir.setReadOnly(True)
	
	save_as.textChanged.connect(lambda:change_dir(save_as.text(),output_dir))
	new_dir.clicked.connect(lambda:get_dir(new_dir,output_dir))
	edit_dir.triggered.connect(lambda:get_dir(new_dir,output_dir))

	frame1_0_layout.addRow("Save as: ",save_as)
	frame1_0_layout.addRow("Change dir: ",new_dir)
	frame1_0_layout.addRow("Output Directory:",output_dir)
	frame1_0_layout.addRow(start_record)
	frame1_0_layout.addRow(play_record)
	
	#frame1_0.addRow(QLabel("two"))
	#frame2_object = recorder("mm")
	

	frame1_1_layout.addWidget(frame1_1_1)
	#frame1_1_layout.addWidget(slider)

	left_layout = QVBoxLayout()
	right_layout = QHBoxLayout()
	frame1_layout = QVBoxLayout()

	#frame2_layout = QVBoxLayout()
	#frame2.setLayout(frame2_layout)
	#frame2_layout.addWidget(frame2_0)
	play_record.setEnabled(False)
	
	#start_record.clicked.connect(lambda:Recorder(frame2,frame2_0,right_layout,start_record,log,save_as.text(),r))	
	start_record.clicked.connect(lambda:recorder(start_record,save_as.text(),play_record))
	#start_record.setText("Stop Recording")
	play_record.clicked.connect(lambda:play(frame2_0,frame2,right_layout,start_record,save_as.text()))
	left_layout.addLayout(frame1_layout)
	frame = QVBoxLayout()
	frame.addWidget(frame1)
	
	frame1_layout.addWidget(frame1_0,alignment=QtCore.Qt.AlignLeft)
	frame1_layout.addWidget(frame1_1,alignment=QtCore.Qt.AlignLeft)
	#left_layout.addRow(QButton("Name"))

	frame1.setLayout(left_layout)

	right_layout.addWidget(frame2_0)

	main_layout = QHBoxLayout()
	#main_layout.addLayout(left_layout)
	main_layout.addLayout(frame)
	main_layout.addLayout(right_layout)

	
	timer.setInterval(1)
	timer.timeout.connect(lambda:capture(frame2_0,right_layout))
	timer.start()
	
	
	widget.setLayout(main_layout)
	widget.setGeometry(100,60,max_width,max_height)
	#widget.setMaximumSize(max_width,max_height)
	widget.show()
	appresult = app.exec()
	
	sys.exit(appresult)    

def recorder(start,output,play):
	global recording,out,out_file
	if "mp4" not in output:
		output+=".mp4"
	if out_dir not in output:
		if name == "nt":
			output = out_dir+"\\"+output
		else:
			output = out_dir+"/"+output
	print(output)
	if recording == None:
		try:
			os.remove(output)
		except:
			pass
		SCREEN_SIZE = tuple(pyautogui.size())
		resolution = (1200, 800)
		fourcc = cv2.VideoWriter_fourcc(*'MP4V')
		out = cv2.VideoWriter(output, fourcc, 10.0, (SCREEN_SIZE))
		start.setText("Stop Recording")
		recording = True
		log.write("recording started")
		timer.start()
		log.write("Saving output to ",output)
		play.setEnabled(False)
	else:
		if out != None:
			out.release()
			cv2.destroyAllWindows()
			out_file = output
			log.write("File ready at", out_file)
		start.setText("Start Recording")
		recording = None
		timer.stop()
		log.write("recording stopped")
		play.setEnabled(True)

def capture(label,layout):
	if recording != None:
		if "Video" in str(layout.itemAt(0).widget()):
			widget = layout.itemAt(0).widget()
			#layout.removeItem(layout.takeAt(0))
			
		label.clear()
		#label.setPixmap(QPixmap())
		layout.removeItem(layout.takeAt(0))
		#label = Qlabel()
		#log.write("capturing---------")  
		img = pyautogui.screenshot()
		qim = ImageQt(img)
		pix = QPixmap.fromImage(qim)
		label.setPixmap(pix)
		layout.addWidget(label)
		if out != None:
			img = np.array(img)
			img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
			out.write(img)

def play(label,frame2,layout,start,output):
	global recording,out,out_file
	log.write("playing from: ",out_file)
	if extension not in output:
		output+=extension
	if out_file != None:
		label = QVideoWidget()
		layout.removeItem(layout.takeAt(0))
		frame2.setVideoOutput(label)
		#label.show()
		layout.addWidget(label)
		frame2.play()
		frame2.setSource(QUrl(out_file))
		frame2.play()
	else:
		start.setText("Start Recording")
		recording = None
		timer.stop()
		log.write("recording stopped")
		if out != None:
			out.release()
			cv2.destroyAllWindows()
			if "mp4" not in output:
				output+=".mp4"
			if out_dir not in output:
				if name == "nt":
					output = out_dir+"\\"+output
				else:
					output = out_dir+"/"+output
			"""
			if name == "nt":
				out_file = out_dir+"\\"+str(output)
			else:
				out_file = out_dir+"/"+str(output)
			"""
			log.write("File ready at", out_file)
			play(label,frame2,layout,start,output)
#@slot
def change_dir(txt,output):
	global out_dir
	if len(txt) < 1:
		txt = random.randint(0,100001)
	
	if name == "nt":
		#out_dir = out_dir+"\\"+str(txt)+extension
		output.setText(out_dir+"\\"+str(txt)+extension)
	else:
		#out_dir = out_dir+"/"+str(txt)+extension
		output.setText(out_dir+"\\"+str(txt)+extension)

def get_dir(btn,out):
	global out_dir
	name = QFileDialog.getExistingDirectory()
	if len(name) > 0:
		btn.setText(name)
		if log != None:
			log.write("Changed saving directory: ",name)
		out_dir = name
		out.setText(name)
	else:
		log.write("Could not set current directory")
def exit_gracefully(app):
	app.quit()
	sys.exit(0)

#signal.signal(signal.SIGINT, sigint_handler)
if __name__=="__main__":
	
	try:
		
		launch(app)
	except KeyboardInterrupt:
		exit_gracefully(app)
	


