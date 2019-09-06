#For Python3
#Import essential modules:
from PyQt5.QtWidgets import QLineEdit,QTableWidget, QWidget, QApplication, QMainWindow, QTableWidgetItem, QVBoxLayout, QScrollBar, QHBoxLayout,QPushButton,QLabel, QTextEdit
from PyQt5 import QtCore

import psutil
import os
import sys
import time

class MyTasks(QWidget):
	def __init__(self,r,c):
		self.r = r
		self.c = c
		super().__init__()


		self.l0 = QLineEdit()
		self.b1 = QPushButton("End Process   >>")
		self.b1.setFixedWidth(300)
		self.b1.clicked.connect(self.end_proc)
		self.notif = QLineEdit()


		self.l1 = QLabel("Processes : ")
		self.l2 = QLabel("Physical memory :")
		self.l3 = QLabel("CPU usage: ")

		self.form_widget = QTableWidget()
		self.form_widget.setRowCount(len(dataset.ids) + 1)
		self.form_widget.setColumnCount(5)
		self.form_widget.setColumnWidth(0, 250)
		self.form_widget.setColumnWidth(1, 90)
		self.form_widget.setColumnWidth(2, 120)
		self.form_widget.setColumnWidth(3, 90)
		self.form_widget.setColumnWidth(4, 90)
		self.headers = ["NAME", "PID", "USER", "CPU", "MEM"]
		self.form_widget.setHorizontalHeaderLabels(self.headers)

		self.setTable()
		QtCore.QTimer.singleShot(1000, lambda: self.Refresh())

		h0_box = QHBoxLayout()
		h0_box.addWidget(self.b1)
		h0_box.addWidget(self.l0)

		h1_box = QHBoxLayout()
		h1_box.addWidget(self.l1)
		h1_box.addSpacing(2)
		h1_box.addWidget(self.l3)
		h1_box.addSpacing(2)
		h1_box.addWidget(self.l2)

		v_box = QVBoxLayout()
		v_box.addWidget(self.form_widget)
		v_box.setSpacing(5)
		v_box.addLayout(h1_box)
		v_box.setSpacing(5)
		v_box.addLayout(h0_box)
		v_box.setSpacing(5)
		v_box.addWidget(self.notif)

		h2_box = QHBoxLayout()
		h2_box.addLayout(v_box)


		self.setWindowTitle("Tasks Manager")
		self.setLayout(h2_box)
		self.setGeometry(100, 100, 600, 600)

	def setTable(self):
		dataset.update()
		mem_percent = 0
		for row in range(0, len(dataset.ids) - 1, 1):
			id = QTableWidgetItem(str(dataset.ids[row]))
			name = QTableWidgetItem(str(dataset.names[row]))
			user = QTableWidgetItem(str(dataset.users[row]))
			cpu = QTableWidgetItem(str(dataset.cpu_percent[row]))
			mem = QTableWidgetItem(str("%.3fk"%(dataset.memory_percent[row])))
			mem_percent += psutil.Process(dataset.ids[row]).memory_percent()
			self.form_widget.setItem(row, 0, name)
			self.form_widget.setItem(row, 1, id)
			self.form_widget.setItem(row, 2, user)
			self.form_widget.setItem(row, 3, cpu)
			self.form_widget.setItem(row, 4, mem)
		self.l1.setText("Processes : " + str(len(dataset.ids)))
		self.l3.setText("CPU Usage : " + str(psutil.cpu_percent())+ "%")
		self.l2.setText("Physical memory : %.2f" %(mem_percent) + "%" )


	def init_ui(self):
			self.show()

	def Refresh(self):
		self.setTable()
		QtCore.QTimer.singleShot(1000, lambda : self.Refresh())
		self.init_ui()

	def end_proc(self):
		id = int(self.l0.text())
		os.kill(id, 1)
		self.notif.setText("Killed " + str(psutil.Process(id).name()) + "\n")

#Class processes id:
class Dataset():
	def __init__(self):
		self.ids = (psutil.pids())
		self.names = [psutil.Process(id).name() for id in self.ids ]
		self.users = [psutil.Process(id).username() for id in self.ids]
		self.cpu_percent = [psutil.Process(id).cpu_percent() for id in self.ids]
		self.memory_percent = [psutil.Process(id).memory_percent()*41.94304 for id in self.ids]
	def update(self):
		self.ids = (psutil.pids())
		self.names = [psutil.Process(id).name() for id in self.ids]
		self.users = [psutil.Process(id).username() for id in self.ids]
		self.cpu_percent = [psutil.Process(id).cpu_percent()*100 for id in self.ids]
		self.memory_percent = [psutil.Process(id).memory_percent()*41.94304 for id in self.ids]
app = None
dataset = Dataset()
def main ():
	global app
	app = QApplication(sys.argv)
	tasks = MyTasks(len(dataset.ids)+1,4)
	app.exec_()

if __name__ == "__main__" :
		main()


