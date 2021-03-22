
# Simple timer for the clocks
# (C) KA 2020

import time
import math

class Timer:

	# Fields

	initialValue = 0
	refValue = 0
	isRunning = False
	isForward = True


	#
	# Constructor
	#
	def __init__(self, isForward = True, initialValue = 0):
		self.isForward = isForward
		self.initialValue = initialValue

	# Start the timer.
	def start(self):
		self.refValue = time.perf_counter()
		self.isRunning = True

	# Stop the timer.
	def stop(self):
		self.initialValue = self.totalSeconds()
		self.isRunning = False

	# Set timer value.
	def set(self, secs):
		self.initialValue = secs
		self.refValue = time.perf_counter()


	def totalSeconds(self):
		if (self.isRunning):
			if (self.isForward):
				return self.initialValue + time.perf_counter() - self.refValue
			else:
				value = self.initialValue - time.perf_counter() + self.refValue
				
				if (value <= 0):
					value = 0
					self.isRunning = False
					self.initialValue = 0

				return value

		else:
			return self.initialValue

	# Called by the shotclock display
	def formatSeconds(self):

		#FIX KA 20210124: Show 1/10 seconds at the last 5 seconds.
		if (self.totalSeconds() < 5):
			return '{:3.1f}'.format(self.totalSeconds())
		else:
			return str(math.trunc(self.totalSeconds())) # '{:1.0f}'.format(self.totalSeconds())

	# Called by the timeout clock display
	def seconds(self):
		#return '{:d}'.format(int(self.totalSeconds()))
		return '{:1.0f}'.format(self.totalSeconds())


	# Called by the shotclock dispatch
	def secondsFull(self):
		return '{:3.1f}'.format(self.totalSeconds()) 


	# Called by the gameclock display
	def formatTime(self):

		hours, remainder = divmod(self.totalSeconds(), 3600)
		minutes, seconds = divmod(remainder, 60)

		if (minutes < 1):
			return '{:02d}:{:04.1f}'.format(int(minutes), seconds) 
		else:
			return '{:02d}:{:02.0f}'.format(int(minutes), math.floor(seconds)) 


	# Called by the gameclock dispatch 
	def formatTimeFull(self):

		hours, remainder = divmod(self.totalSeconds(), 3600)
		minutes, seconds = divmod(remainder, 60)

		return '{:02d}:{:010.7f}'.format(int(minutes), seconds) 		


	# FIX KA 20210214: return fractional seconds to sync gameclock and shotclock
	def fractionalSeconds(self):

		return self.totalSeconds() % 1
		
