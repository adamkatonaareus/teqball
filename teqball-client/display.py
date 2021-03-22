
# Display base class.
# (C) KA 2020

import config as CONFIG
import pygame
import log4p
import os

class Display:

	log = None
	screen = None
	status = None

	statusFont = None
	statusRec = None
	doInit = True

	#
	# Constructor
	#
	def __init__(self, status):

		logger = log4p.GetLogger(__name__, config=CONFIG.LOG4P_CONFIG)
		self.log = logger.logger
		self.log.info("Initializing Display...")

		# Init pygame, get the screen surface
		os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
		pygame.init()
		self.log.debug(pygame.display.Info())
		
		# Don't do this, it's slower.
#		self.screen = pygame.display.set_mode((0, 0), pygame.NOFRAME | pygame.HWSURFACE | pygame.DOUBLEBUF) #FULLSCREEN)
		self.screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
		pygame.mouse.set_visible(False)

		self.status = status

		self.statusFont = pygame.font.Font(pygame.font.get_default_font(), 120)
		self.statusRect = pygame.Rect(0, 0, CONFIG.DISPLAY_WIDTH, CONFIG.DISPLAY_HEIGHT)


	def startup(self):

		self.log.info("Starting Display...")


	def shutdown(self):

		self.log.info("Shutting down Display...")
		pygame.quit()


	# Draw status when not connected.
	def drawStatus(self):

		self.screen.fill(CONFIG.BACKGROUND_COLOR, self.statusRect)

		if (self.status.mqttConnected == False):

			surface = self.statusFont.render("Not connected.", True, (255, 255, 255))
			self.screen.blit(surface, (0, 0))


	# Clear the whole display
	def clear(self):

		#FIX KA 20210322: Don't do this, background will erase all content.
		pass
		#fullRect = pygame.Rect(0, 0, CONFIG.DISPLAY_WIDTH, CONFIG.DISPLAY_HEIGHT)
		#self.screen.fill(CONFIG.BACKGROUND_COLOR, fullRect)
		#pygame.display.update(fullRect)
