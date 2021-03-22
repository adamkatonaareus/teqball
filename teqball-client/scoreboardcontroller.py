#
# Scoreboard controller.
# (C) KA 2021
#

import config as CONFIG
import status
import controller
import log4p
import datetime

#
# Class to control the scoreboard.
#
class ScoreBoardController(controller.Controller):

	#
	# Constructor
	#
	def __init__(self, status):

		super().__init__(status)
		self.log.info("Initializing ScoreBoardController...")


	def startup(self):

		self.log.info("Starting ScoreBoardController...")


	def shutdown(self):

		self.log.info("Shutting down ScoreBoardController...")


	# Update scoreboard
	def update(self):

		return


	#
	# Process incoming message.
	#
	def onMessage(self, message):

		# FIX KA 20210116: checking if message has the module key. Pingback has no module key.
		if ("module" in message and message["module"] != "" and message["module"] != "scoreboard"):
			self.log.debug("Skipping message to module " + message["module"])
			return

		if ("isSync" in message and message["isSync"]):
			self.log.debug("Skipping sync message.")
			return

		self.log.debug("ScoreBoard command: " + message["command"])

		switcher = {
			"setteamname": self.setTeamName,
			"setteampoints": self.setTeamPoints,
			"ping": self.ping,
			"reset": self.reset
		}	

		try:

			func = switcher.get(message["command"], self.dummy)
			func(message)

		except Exception as e:
				log.error("Unexpected error: " + str(e))
				log.error(e)



	def setTeamName(self, params):

		self.log.debug("Setting team " + str(params["teamId"]) + " name to " + params["value"])

		self.status.teamName[int(params["teamId"])-1] = params["value"]
		self.status.display.doDrawTeamPoints = True


	def setTeamPoints(self, params):

		self.log.debug("Setting team " + str(params["teamId"]) + " points to " + str(params["value"]))

		value = int(params["value"])
		if (value < 0):
			value = 0

		self.status.teamPoints[int(params["teamId"])-1] = value
		self.status.display.doDrawTeamPoints = True

		self.ping(params)


	def ping(self, params):

		# Only do this if we are the bosses.
		if (CONFIG.CLIENT_MODE == "main" and CONFIG.CLIENT_ID == 1):

			self.log.debug("Sending back scoreboard data...")
			message = {

				"module": "scoreboard",
			  	"command": "setboard",
			  	"isSync": True,

				"teamName": self.status.teamName,
				"teamPoints": self.status.teamPoints,
			}

			self.status.mqttClient.publish(message)


	def reset(self, params):

		# Re-init display
		self.log.debug("Resetting scoreboard.")
		self.status.display.doDrawScoreBoard = True
		self.status.display.doDrawGameClock = True
		self.ping(params)


	def dummy(self, params):

		self.log.debug("ScoreBoardController - not processing: " + params["command"])

