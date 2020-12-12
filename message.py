'''The datetime helps to make sure that the current date and time is in use. And the message
class is the blue print to hold the message object and its properties'''

import datetime

class Message:

	def __init__(self,msg):
		self.msg = msg
		self.datetime = datetime.datetime.now()
		self.to = None
		self.fr = None

	def __repr__(self):
		return"{} at this {}".format(self.msg, self.datetime)
