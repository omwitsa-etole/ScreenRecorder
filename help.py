from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QLabel
from PySide6.QtWidgets import *
from PySide6 import *
from PySide6.QtWebEngineWidgets import * 
from PySide6.QtGui import *

class newWindow(QWidget):
	def __init__(self):
		super().__init__()
		widget = QTextEdit()
		widget.setReadOnly(True)
		widget.setStyleSheet("border: 1px solid white;border-radius: 4px;text-align:center;")
		widget.append("Display help message")
		layout = QVBoxLayout()
		layout.addWidget(widget)
		self.setLayout(layout)
		self.setWindowTitle("Application Help")
	def exit(self):
		pass

class Help(QMainWindow):
	def __init__(self,parent,log):
		
		super().__init__()
		#self.setGeometry(100,60,140,140)
		#self.show()
		w = newWindow()
		w.show()
		log.write(w)
		log.write("Opened help tab")
	
