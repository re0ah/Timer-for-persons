def if_valid_text_time(text):
	valid_chars = ['0', '1', '2', '3', '4', ':',
				   '5', '6', '7', '8', '9']
	for c in text:
		if (c not in valid_chars):
			return False
	return True

class Time():
	"""allow only minutes & seconds"""
	def __init__(self, min=0, sec=0, text=None):
		if text == None:
			self.min = min
			self.sec = sec
		else:
			if text == "":
				self.min = 0
				self.sec = 0
			elif (':' in text):
				text_split = text.split(':')
				self.min = int(text_split[0])
				self.sec = int(text_split[1])
			else:
				self.min = int(text)
				self.sec = 0
		self.normalize()
	
	def normalize(self):
		min_in_sec = self.sec // 60
		self.min += min_in_sec
		self.sec = self.sec - (60 * min_in_sec)
		if self.min < 0:
			self.min = 0
			self.sec = 0

	def add(time_1, time_2):
		if isinstance(time_2, Time):
			time_1.min += time_2.min
			time_1.sec += time_2.sec
		if isinstance(time_2, int):
			time_1.min += time
		time_1.normalize()
		return time_1

	def __add__(self, time):
		t = Time(self.min, self.sec)
		return t.add(time)

	def __iadd__(self, time):
		return self.add(time)

	def sub(time_1, time_2):
		if isinstance(time_2, Time):
			time_1.min -= time_2.min
			time_1.sec -= time_2.sec
		if isinstance(time_2, int):
			time_1.min -= time
		time_1.normalize()
		return time_1

	def __sub__(self, time):
		t = Time(self.min, self.sec)
		return t.sub(time)

	def __isub__(self, time):
		return self.sub(time)

	def __eq__(self, time):
		min_cmp = (self.min == time.min)
		sec_cmp = (self.sec == time.sec)
		return (min_cmp & sec_cmp)

	def __str__(self):
		if self.sec > 9:
			str_sec = str(self.sec)
		else:
			str_sec = "0" + str(self.sec)
		if self.min > 9:
			str_min = str(self.min)
		else:
			str_min = "0" + str(self.min)
		return str_min + ':' + str_sec