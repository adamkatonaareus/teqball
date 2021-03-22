#
# Controller base class.
# (C) KA 2020
#

import config as CONFIG
import status
import log4p


#
# Main controller class.
#
class Controller:

	log = None
	status = None

	#
	# Constructor
	#
	def __init__(self, status):

		logger = log4p.GetLogger(__name__, config=CONFIG.LOG4P_CONFIG)
		self.log = logger.logger
		self.status = status

	#
	# This is an abstract method...
	#
	def update(self):

		self.log.debug("Nothing to do!")

	#
	# Process incoming message.
	#
	def onMessage(self, message):

		self.log.debug("Nothing to do!")
		
