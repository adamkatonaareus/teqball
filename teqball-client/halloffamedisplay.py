
# Hall of fame display
# (C) KA 2020

import config as CONFIG
import display
import pygame
import log4p
import time
import datetime
import math


class HallOfFameDisplay(display.Display):

	titleFont = None
	rowFont = None

	doDraw = True

	# Always drawing full screen
	fullRect = None

	#
	# Constructor
	#
	def __init__(self, status):

		super().__init__(status)
		self.log.info("Initializing HallOfFameDisplay...")

		# Init fonts
		self.titleFont = pygame.font.Font(CONFIG.FONT_FOLDER + CONFIG.HOF_TITLE_FONT_TYPE, CONFIG.HOF_TITLE_FONT_SIZE)
		self.rowFont = pygame.font.Font(CONFIG.FONT_FOLDER + CONFIG.HOF_ROW_FONT_TYPE, CONFIG.HOF_ROW_FONT_SIZE)

		# Calculate dirty rects
		self.fullRect = pygame.Rect(0, 0, CONFIG.DISPLAY_WIDTH, CONFIG.DISPLAY_HEIGHT)

		self.background = pygame.image.load(CONFIG.IMAGE_FOLDER + "background.png").convert()
		

	def startup(self):

		self.log.info("Starting HallOfFameDisplay...")


	def shutdown(self):

		self.log.info("Shutting down HallOfFameDisplay...")
		super().shutdown()


	# Main draw method.
	def draw(self):

		dirtyRects = []

		if (self.status.mqttConnected == False):
			self.drawStatus()
			dirtyRects.append(self.statusRect)
			self.doInit = True

		else:		

			# Draw all when reinited.
			if (self.doInit):
				self.doInit = False
				self.clear()

				pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(0, 0, CONFIG.DISPLAY_WIDTH, CONFIG.DISPLAY_HEIGHT), 1)
				pygame.display.flip()
								
				self.doDraw = True

			if (self.doDraw):
				self.doDraw = False	
				self.drawFull()
				dirtyRects.append(self.fullRect)

		pygame.display.update(dirtyRects)


	# Draw the Hall of fame
	def drawFull(self):

		self.screen.blit(self.background, (CONFIG.BACKGROUND_LEFT, CONFIG.BACKGROUND_TOP))
		#self.screen.fill(CONFIG.BACKGROUND_COLOR, self.fullRect)

		text = "Hall of Fame"
		size = self.titleFont.size(text)
		position = ((CONFIG.DISPLAY_WIDTH - size[0])/2, CONFIG.HOF_TITLE_TOP)
		self.write(text, position, self.titleFont, CONFIG.HOF_TITLE_COLOR)
		self.log.debug("Drawn.")


	def write(self, text, position, font, color):

		surface = font.render(text, True, color)
		self.screen.blit(surface, position)