# Timer used to estimate function run time
import datetime as dt

class timer:
	create_time = -1
	time_stamps = []
	time_int = []
	time_label = []
	total_sec = 0
	avg_sec = 0
	
	def __init__ (self):
		self.time_stamps = []
		self.time_int = []
		self.time_label = []
		self.total_sec = 0
		self.avg_sec = 0
		self.create_time = dt.datetime.now()
		self.time_stamps.append(self.create_time)
	
	def lap (self, label=''):
		self.time_stamps.append(dt.datetime.now())
		last_int = (self.time_stamps[-1] - self.time_stamps[-2]).total_seconds()
		self.time_int.append(last_int)
		self.total_sec += last_int
		self.avg_sec = self.total_sec / len(self.time_int)
		if label == '':
			self.time_label.append(str(len(self.time_int)+1))
		else:
			self.time_label.append(label)
	
	def format_time (self, t):
		mins = int(t / 60)
		secs = int(t - mins * 60)
		hrs = 0
		if(mins > 60): 
			hrs = int(mins/60)
			mins = mins - hrs * 60
		return [hrs, mins, secs]