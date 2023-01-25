import threading
import time
from trycourier import Courier

class ThreadedMessenger(object):
	def __init__(self, auth_token, slack_auth_token, to_details, interval, message_type='email'):
		self.interval = interval
		self.slack_auth_token = slack_auth_token
		self.auth_token = auth_token
		self.to_details = to_details
		self.message_type = message_type
		thread = threading.Thread(target=self.run, args=())
		thread.daemon = True
		thread.start()

	def send_slack(self):
		client = Courier(auth_token=self.auth_token)
		resp = client.send_message(
			message={
				"to": {
					"slack": {
						"access_token": self.slack_auth_token,
						"channel": "C04KW6QLPM5",
					},
				},
				"template": "SQJNQEBW7ZMHZJPR06X434M076BS",
					"data": {
						"apt_date": self.to_details['timeDetails'],
						"apt_time": self.to_details['eventDetails'],
					},
				})

	def send_email(self):
		client = Courier(auth_token=self.auth_token)
		resp = client.send_message(
			message={
			"to": {
				"email": self.to_details['email']
				},
			"template": "N7MYVF5PWS4J2EKKG4HAYBVSM2CW",
				"data": {
					"name": self.to_details['name'],
					"timeDetails": self.to_details['timeDetails'],
					"eventDetails": self.to_details['eventDetails'],
					},
			})

	def run(self):
		time.sleep(self.interval)
		if self.message_type=='email':
			self.send_email()
		elif self.message_type=='slack':
			self.send_slack()

