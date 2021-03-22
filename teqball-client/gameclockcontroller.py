#
# Game clock controller.
# (C) KA 2020
#

import config as CONFIG
import status
import controller
import log4p
import datetime

#
# Class to control the game clock.
# Used by the shot clock display and the scoreboard too.
#
class GameClockController(controller.Controller):

	oldGameClockValue = 0
	isSignalDone = False


	#
	# Constructor
	#
	def __init__(self, status):

		super().__init__(status)
		self.log.info("Initializing GameClockController with id " + str(CONFIG.CLIENT_ID))


	def startup(self):

		self.log.info("Starting GameClockController...")


	def shutdown(self):

		self.log.info("Shutting down GameClockController...")


	# Update clock
	def update(self):

		# Only update the clock when a second elapsed
		if (int(self.status.gameClock.totalSeconds()) != self.oldGameClockValue):
			self.status.display.doDrawGameClock = True
			self.dispatchTime()

		# Or always update when time is less than a minute.
		elif (self.status.gameClock.isRunning and self.status.gameClock.totalSeconds() < 60):
			self.status.display.doDrawGameClock = True
			self.dispatchTime()

		self.oldGameClockValue = int(self.status.gameClock.totalSeconds())



	#
	# Process incoming message.
	#
	def onMessage(self, message):

		if ("module" in message and message["module"] != "" and message["module"] != "gameclock" and message["command"] != "signal"):
			self.log.debug("Skipping message to module " + message["module"])
			return

		# FIX KA 20210116: we need to allow signal messages from both sources: shotclock and gameclock 
		if ("isSync" in message and message["isSync"]):
			if (message["command"] == "signal"): # and message["module"] == "shotclock"):
				self.log.debug("Allowing signal.")
			else:
				self.log.debug("Skipping sync message.")
				return

		self.log.debug("GameClock command: " + message["command"])

		switcher = {
			"start": self.start,
			"stop": self.stop,
			"settime": self.setTime,
			"ping": self.ping,
			"reset": self.reset,
		}	

		func = switcher.get(message["command"], self.dummy)
		func(message)



	def start(self, params):

		self.log.debug("Starting game clock.")

		if (self.status.gameClock.totalSeconds() == 0):
			self.status.gameClock.set(CONFIG.GAMECLOCK_START_SECS)

		self.status.gameClock.start()
		self.status.display.doDrawGameClock = True
		self.oldGameClockValue = int(self.status.gameClock.totalSeconds())

		self.dispatchTime()


	def stop(self, params):

		self.log.debug("Stopping game clock.")
		self.status.gameClock.stop()

		self.dispatchTime()


	def setTime(self, params):

		self.log.debug("Setting game clock time.")
		values = params["value"].split(":")
		self.status.gameClock.set(int(values[0]) * 60 + float(values[1]))
		self.status.display.doDrawGameClock = True
		self.log.debug("Time set to " + str(self.status.gameClock.totalSeconds()) + " secs.")


	def ping(self, params):

		# Send back current time and quarter.
		self.log.debug("Sending back game clock time and quarter.")
		self.dispatchTime()


	def reset(self, params):

		# Re-init display
		self.log.debug("Resetting game clock.")
		self.status.display.doDrawGameClock = True
		self.dispatchTime()


	def dummy(self, params):

		self.log.debug("GameClockController - not processing: " + params["command"])


	#
	#	RPI's aren't in sync because they get the start-stop messages delayed.
	#	We need this method to sync all game clocks.
	#
	def dispatchTime(self):

		# Only do this if we are the bosses.
		if (CONFIG.CLIENT_MODE == "main" and CONFIG.CLIENT_ID == 1):

			message = {
				"module": "gameclock",
			  	"command": "settime",
			  	"value": self.status.gameClock.formatTimeFull(),
			  	"isSync": True
			}	

			self.status.mqttClient.publish(message)
