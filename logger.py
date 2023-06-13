from PySide6.QtWidgets import *
from PySide6 import *
class OutLog(QTextEdit):
	def __init__(self):
		#self.edit = edit
		super().__init__()
		self.setReadOnly(True)
		self.setDocumentTitle("LOGGER")
	def write(self,*m):
		self.append(' '.join(m))
