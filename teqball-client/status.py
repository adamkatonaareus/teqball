
# Current status
# (C) KA 2021

import config as CONFIG
import time
import datetime
import timer


class Status:

	# Global objects
	display = None
	mqttClient = None
	mainController = None
	gameClockController = None
	mqttConnected = False
	isHalting = False

	hallOfFameDisplay = None
	winnerDisplay = None
	hallOfFameInterval = 0
	displayMode = 0
	

	#
	# Constructor
	#
	def __init__(self):
		self.reset()

	#
	# Reset all values.
	#
	def reset(self):

		self.gameClock = timer.Timer(isForward = False, initialValue = CONFIG.GAMECLOCK_START_SECS)

		self.teamName = ["Team 1", "Team 2"]
		self.teamPoints = [0, 0]
