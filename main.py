from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QListWidgetItem
from PyQt5.QtCore import QThread, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from count_time import Time
import sys
import count_time
import time
import os

class List_data_widgets():
	def __init__(self):
		self.person_list = []

	def num_of_person(self):
		return len(self.person_list)

	def add_person(self, dict):
		self.person_list.append(dict)

	def timer_state(self, row):
		return self.person_list[row]["timer"]

	def timer_state_invert(self, widget):
		index = self.get_index_widget(widget)
		self.person_list[index]["timer"] = not self.person_list[index]["timer"]

	def set_timer_state(self, row, state):
		self.person_list[row]["timer"] = state

	def time(self, row):
		return self.person_list[row]["time"]

	def add_time(self, widget, _time):
		index = self.get_index_widget(widget)
		self.person_list[index]["time"] += _time
		time_text = str(self.person_list[index]["time"])
		widget.lbl_time.setText(time_text)

	def sub_time(self, widget, _time):
		index = self.get_index_widget(widget)
		self.person_list[index]["time"] -= _time
		time_text = str(self.person_list[index]["time"])
		widget.lbl_time.setText(time_text)

	def sub_time_index(self, index, _time):
		self.person_list[index]["time"] -= _time
		time_text = str(self.person_list[index]["time"])
		self.person_list[index]["widget"].lbl_time.setText(time_text)

	def get_index_widget(self, widget):
		for i in range(self.num_of_person()):
			if self.person_list[i]["widget"] == widget:
				return i

	def get_index_item(self, item):
		for i in range(self.num_of_person()):
			if self.person_list[i]["item"] == item:
				return i

	def get_widget(self, item):
		for i in self.person_list:
			if i["item"] == item:
				return i["widget"]

	def find(self, val, key):
		for i in self.person_list:
			if i[key] == val:
				return True
		return False

class Sound_thread(QThread):
	def __init__(self, fname, volume):
		super().__init__(None)
		self.player = QMediaPlayer()
		self.player.setMedia(QMediaContent(QUrl(fname)))
		self.player.setVolume(volume)

	def run(self):
		self.player.play()

class Counter_thread(QThread):
	def __init__(self, data, mainw):
		super().__init__(None)
		self.data = data
		self.mainw = mainw
		self.window = mainw.window

	def run(self):
		st = Sound_thread("sound.mp3", self.window.volume_slider.value())
		while True:
			time.sleep(1)
			for i in range(self.data.num_of_person()):
				if self.data.timer_state(i) == False:
					continue
				elif self.data.time(i) == Time(0, 0):
					self.data.set_timer_state(i, False)
					self.mainw.set_widget_style(self.data.person_list[i]["widget"], "time_end")
					st.start()
				else:
					self.data.sub_time_index(i, Time(0, 1))

class MainW(QMainWindow):
	def __init__(self):
		super().__init__(None)
		self.tb_data = List_data_widgets()
		self.init_window()
		self.counter_thread = Counter_thread(self.tb_data, self)
		self.counter_thread.start()

	def init_window(self):
		self.window = uic.loadUi(os.path.join("ui", "mainw.ui"))
		self.window.show()
		self.window.btn_add_person.clicked.connect(self.add_person)
		self.window.le_add_person.returnPressed.connect(self.add_person)
		self.window.btn_delete_person.clicked.connect(self.delete_person)
		self.window.btn_add_time.clicked.connect(self.add_time)
		self.window.btn_sub_time.clicked.connect(self.sub_time)
		self.window.le_add_time.returnPressed.connect(self.add_time)
		self.window.list_widget.itemPressed.connect(self.select_widget)
		self.window.list_widget.itemDoubleClicked.connect(self.start_count)

	style_widget = {
					"normal": "background: #CACACA;border-bottom: 2px solid #111111;",
					"selected": "background: #A0A0A0;border-bottom: 2px solid #111111;",
					"time_end": "background: #AA1515;border-bottom: 2px solid #111111;"
					}
	style_widget_lbl = {
						"lbl_pos":
						{
							"normal": "background: #D0D0D0;border: 2px solid #111111;color: #111111",
							"selected": "background: #757575;border: 2px solid #111111;color: #FAFAFA",
							"time_end": "background: #802222;border: 2px solid #111111;color: #FFFFFF",
						},
						"lbl_name":
						{
							"normal": "background: #D0D0D0;border: 2px solid #111111;color: #111111",
							"selected": "background: #757575;border: 2px solid #111111;color: #FAFAFA",
							"time_end": "background: #802222;border: 2px solid #111111;color: #FFFFFF",
						},
						"lbl_time":
						{
							"normal": "background: #D0D0D0;border: 2px solid #111111;border-left: None;color: #111111",
							"selected": "background: #757575;border: 2px solid #111111;border-left: None;color: #FAFAFA",
							"time_end": "background: #802222;border: 2px solid #111111;border-left: None;color: #FFFFFF"
						}
					}
	selected_widget = None
	def select_widget(self, item):
		if self.selected_widget != None:
			self.set_widget_style(self.selected_widget, "normal")
		widget = self.tb_data.get_widget(item)
		self.set_widget_style(widget, "selected")
		self.selected_widget = widget

	def set_widget_style(self, widget, style):
		widget.setStyleSheet(self.style_widget[style])
		widget.lbl_pos.setStyleSheet (self.style_widget_lbl["lbl_pos"][style])
		widget.lbl_name.setStyleSheet(self.style_widget_lbl["lbl_name"][style])
		widget.lbl_time.setStyleSheet(self.style_widget_lbl["lbl_time"][style])

	def add_person(self):
		time_text = self.window.le_add_time.text()
		text = self.window.le_add_person.text()
		if (count_time.if_valid_text_time(time_text) == False) |\
		   (text == "") | (self.tb_data.find(text, "name")):
			return
		_time = Time(text=time_text)
		num_row = self.tb_data.num_of_person()

		self.tb_data.add_person({"name": text,
								 "time": _time,
								 "timer": False,
								 "item": None,
								 "widget": None}
		)
		self.tb_data.person_list[num_row]["item"] = QListWidgetItem()
		self.tb_data.person_list[num_row]["widget"] = uic.loadUi(os.path.join("ui", "widget.ui"))
		size = self.tb_data.person_list[num_row]["widget"].sizeHint()
		self.tb_data.person_list[num_row]["item"].setSizeHint(size)
		self.window.list_widget.addItem(self.tb_data.person_list[num_row]["item"])
		self.window.list_widget.setItemWidget(self.tb_data.person_list[num_row]["item"],
											  self.tb_data.person_list[num_row]["widget"])
		self.tb_data.person_list[num_row]["widget"].lbl_pos.setText(str(num_row + 1))
		self.tb_data.person_list[num_row]["widget"].lbl_name.setText(text)
		self.tb_data.person_list[num_row]["widget"].lbl_time.setText(str(_time))

	def delete_person(self):
#		pass
#		import gc
		item = self.window.list_widget.currentItem()
		if item == None:
			return
		index = self.tb_data.get_index_item(item)
		if index == None:
			return
		del self.tb_data.person_list[index]
		for i in range(self.tb_data.num_of_person()):
			self.tb_data.person_list[i]["widget"].lbl_pos.setText(str(i + 1))
		item.setHidden(True)
		#self.window.list_widget.removeItemWidget(item)
#		gc.collect()

	def add_time(self):
		time_text = self.window.le_add_time.text()
		if count_time.if_valid_text_time(time_text) == False:
			return
		self.tb_data.add_time(self.selected_widget, Time(text=time_text))

	def sub_time(self):
		time_text = self.window.le_add_time.text()
		if count_time.if_valid_text_time(time_text) == False:
			return
		self.tb_data.sub_time(self.selected_widget, Time(text=time_text))

	def start_count(self, item):
		if self.selected_widget != None:
			self.tb_data.timer_state_invert(self.selected_widget)
	
if __name__ == "__main__":
	app = QApplication([])
	mainw = MainW()
	sys.exit(app.exec())
