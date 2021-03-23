
# Main method.
# (C) KA 2021

import config as CONFIG
import log4p
import display
import status
import mqttclient
import time
import controller
import scoreboarddisplay
import halloffamedisplay
import winnerdisplay
import scoreboardcontroller
import gameclockcontroller
import os
import traceback
import sqlite3 as sl


logger = log4p.GetLogger(__name__, config=CONFIG.LOG4P_CONFIG)
log = logger.logger

log.info("Initializing TeqBall app...")

# Create object instances
status = status.Status()

# We always need a game clock controller
status.gameClockController = gameclockcontroller.GameClockController(status)

status.display = scoreboarddisplay.ScoreBoardDisplay(status)
status.mainController = scoreboardcontroller.ScoreBoardController(status)

status.hallOfFameDisplay = halloffamedisplay.HallOfFameDisplay(status)
status.winnerDisplay = winnerdisplay.WinnerDisplay(status)

# We need an mqtt client
status.mqttClient = mqttclient.MqttClient(status)

# Start all functions
status.display.startup()
status.hallOfFameDisplay.startup()
status.winnerDisplay.startup()
status.mainController.startup()
status.gameClockController.startup()
status.mqttClient.startup()


log.info("Press Ctrl+C to exit.")


# Stop all stuff.
def doHalt():

	log.info("Shutting down TeqBall app...")
	status.mqttClient.shutdown()
	status.mainController.shutdown()
	status.gameClockController.shutdown()
	status.display.shutdown()
	status.hallOfFameDisplay.shutdown()
	status.winnerDisplay.shutdown()

	# Shut down the RPI too.
	if (status.isHalting):
		os.system("halt")

	quit()


while True:

	try:

		# Idle wait
		time.sleep(CONFIG.MAIN_SLEEP)

		# Change display mode if necessary
		status.hallOfFameInterval = status.hallOfFameInterval + CONFIG.MAIN_SLEEP
		if (status.hallOfFameInterval >= CONFIG.HOF_CHANGE_INTERVAL_SECS):
			status.hallOfFameInterval = 0
			if (status.displayMode == 0):
				#log.debug("Switching to Hall of Fame")
				status.displayMode = 1
				status.hallOfFameDisplay.doDraw = True
			else:
				#log.debug("Switching to Scoreboard")
				status.displayMode = 0
				status.display.doInit = True


		if (status.isHalting):
			doHalt()
		else:
			status.gameClockController.update()
			status.mainController.update()

			if (status.displayMode == 0):
				status.display.draw()
			elif (status.displayMode == 1):
				status.hallOfFameDisplay.draw()
			else:
				status.winnerDisplay.draw()


	except (KeyboardInterrupt):

		doHalt()

	except Exception as e:

		log.error("Unexpected error: " + str(e))
		log.error(e)
		print(traceback.format_exc())
		#raise

