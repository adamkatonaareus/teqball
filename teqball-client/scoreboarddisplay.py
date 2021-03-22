
# Scoreboard display
# (C) KA 2020

import config as CONFIG
import display
import pygame
import log4p
import time
import datetime
import math


class ScoreBoardDisplay(display.Display):

	doDrawGameClock = True
	doDrawTeamPoints = True

	gameClockFont = None
	teamPointsFont = None
	teamFont = None
	labelFont = None

	gameClockRect = None
	side1Rect = None
	side2Rect = None
	background = None

	#
	# Constructor
	#
	def __init__(self, status):

		super().__init__(status)
		self.log.info("Initializing ScoreBoardDisplay...")

		# Init fonts
		self.gameClockFont = pygame.font.Font(CONFIG.FONT_FOLDER + CONFIG.SCOREBOARD_TIME_FONT_TYPE, CONFIG.SCOREBOARD_TIME_FONT_SIZE)
		self.teamFont = pygame.font.Font(CONFIG.FONT_FOLDER + CONFIG.SCOREBOARD_TEAM_FONT_TYPE, CONFIG.SCOREBOARD_TEAM_FONT_SIZE)
		self.labelFont = pygame.font.Font(CONFIG.FONT_FOLDER + CONFIG.SCOREBOARD_LABEL_FONT_TYPE, CONFIG.SCOREBOARD_LABEL_FONT_SIZE)
		self.teamPointsFont = pygame.font.Font(CONFIG.FONT_FOLDER + CONFIG.SCOREBOARD_TEAM_POINTS_FONT_TYPE, CONFIG.SCOREBOARD_TEAM_POINTS_FONT_SIZE)

		# Calculate dirty rects
		labelSize = self.labelFont.size("A")

		size = self.gameClockFont.size("88:88:8")
		self.gameClockRect = pygame.Rect((CONFIG.DISPLAY_WIDTH - size[0]) / 2, CONFIG.SCOREBOARD_TIME_TOP, size[0], size[1])

		size = self.teamFont.size("888")
		self.teamRect = pygame.Rect(CONFIG.SCOREBOARD_TEAM_LEFT, CONFIG.SCOREBOARD_TEAM_TOP, CONFIG.DISPLAY_WIDTH - 2 * CONFIG.SCOREBOARD_TEAM_LEFT, size[1])

		size = self.teamPointsFont.size("888")
		self.teamPointsRect = pygame.Rect(CONFIG.SCOREBOARD_TEAM_POINTS_LEFT, self.teamRect[1] + self.teamRect[3], CONFIG.DISPLAY_WIDTH - 2 * CONFIG.SCOREBOARD_TEAM_POINTS_LEFT, size[1])

		self.background = pygame.image.load(CONFIG.IMAGE_FOLDER + "background.png").convert()


	def startup(self):

		self.log.info("Starting ScoreBoardDisplay...")


	def shutdown(self):

		self.log.info("Shutting down ScoreBoardDisplay...")
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
				
				self.screen.blit(self.background, (CONFIG.BACKGROUND_LEFT, CONFIG.BACKGROUND_TOP))
				pygame.display.flip()

				self.doDrawGameClock = True
				self.doDrawTeamPoints = True

			if (self.doDrawTeamPoints):
				self.doDrawTeamPoints = False	
				self.drawTeamPoints()
				dirtyRects.append(self.teamRect)
				dirtyRects.append(self.teamPointsRect)

			if (self.doDrawGameClock):
				self.doDrawGameClock = False
				self.drawGameClock()
				dirtyRects.append(self.gameClockRect)

		# pygame.draw.rect(self.screen, (0, 255, 0), pygame.Rect(0, 0, CONFIG.DISPLAY_WIDTH, CONFIG.DISPLAY_HEIGHT), 1)

		pygame.display.update(dirtyRects)


	# Draw the game clock
	def drawGameClock(self):

		sbg = pygame.Surface((CONFIG.DISPLAY_WIDTH, self.gameClockRect[3]))
		sbg.blit(self.background, (CONFIG.BACKGROUND_LEFT, CONFIG.BACKGROUND_TOP))
		# self.screen.fill(CONFIG.BACKGROUND_COLOR, self.gameClockRect)

		text = self.status.gameClock.formatTime()
		size = self.gameClockFont.size(text)
		position = ((CONFIG.DISPLAY_WIDTH - size[0])/2, self.gameClockRect[1])
		surface = self.gameClockFont.render(text, True, CONFIG.SCOREBOARD_TIME_COLOR)
		
		sbg.blit(surface, position)
		self.screen.blit(sbg, (0, 0))


	# Draw team points
	def drawTeamPoints(self):

		self.screen.blit(self.background, (CONFIG.BACKGROUND_LEFT, CONFIG.BACKGROUND_TOP))
		#self.screen.fill(CONFIG.BACKGROUND_COLOR, self.teamRect)
		#self.screen.fill(CONFIG.BACKGROUND_COLOR, self.teamPointsRect)

		# Draw team names
		teamSize = self.teamFont.size(self.status.teamName[1])
		self.write(self.status.teamName[0], [self.teamRect[0], self.teamRect[1]], self.teamFont, CONFIG.SCOREBOARD_TEAM_1_COLOR)
		self.write(self.status.teamName[1], [self.teamRect[0] + self.teamRect[2] - teamSize[0], self.teamRect[1]], self.teamFont, CONFIG.SCOREBOARD_TEAM_2_COLOR)

		# Draw points
		text = str(self.status.teamPoints[0])
		self.write(text, self.teamPointsRect, self.teamPointsFont, CONFIG.SCOREBOARD_TEAM_1_COLOR)

		text = str(self.status.teamPoints[1])
		size = self.teamPointsFont.size(text)
		position = (self.teamPointsRect[0] + self.teamPointsRect[2] - size[0], self.teamPointsRect[1])
		surface = self.teamPointsFont.render(text, True, CONFIG.SCOREBOARD_TEAM_2_COLOR)
		self.screen.blit(surface, position)

	def write(self, text, position, font, color):

		surface = font.render(text, True, color)
		self.screen.blit(surface, position)