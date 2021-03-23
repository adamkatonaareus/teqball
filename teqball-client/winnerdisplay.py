
# Winner display
# (C) KA 2020

import config as CONFIG
import display
import pygame
import log4p
import time
import datetime
import math


class WinnerDisplay(display.Display):

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
		self.log.info("Initializing WinnerDisplay...")

		# Init fonts
		self.titleFont = pygame.font.Font(CONFIG.FONT_FOLDER + CONFIG.WINNER_TITLE_FONT_TYPE, CONFIG.WINNER_TITLE_FONT_SIZE)
		self.teamFont = pygame.font.Font(CONFIG.FONT_FOLDER + CONFIG.WINNER_TEAM_FONT_TYPE, CONFIG.WINNER_TEAM_FONT_SIZE)

		# Calculate dirty rects
		self.fullRect = pygame.Rect(0, 0, CONFIG.DISPLAY_WIDTH, CONFIG.DISPLAY_HEIGHT)

		self.background = pygame.image.load(CONFIG.IMAGE_FOLDER + "background.png").convert()
		

	def startup(self):

		self.log.info("Starting WinnerDisplay...")


	def shutdown(self):

		self.log.info("Shutting down WinnerDisplay...")
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

		text = "The winner is"
		size = self.titleFont.size(text)
		position = ((CONFIG.DISPLAY_WIDTH - size[0])/2, CONFIG.WINNER_TITLE_TOP)
		self.write(text, position, self.titleFont, CONFIG.WINNER_TITLE_COLOR)
		
		if (self.status.winner == 1):
			text = self.status.teamName[0]
		else:
			text = self.status.teamName[1]

		size = self.teamFont.size(text)
		position = ((CONFIG.DISPLAY_WIDTH - size[0])/2, CONFIG.WINNER_TEAM_TOP)
		self.write(text, position, self.teamFont, CONFIG.WINNER_TEAM_COLOR)


	def write(self, text, position, font, color):

		surface = font.render(text, True, color)
		self.screen.blit(surface, position)