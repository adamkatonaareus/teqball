
# Configuration


import pygame

CLIENT_MODE = "main"
CLIENT_ID = 1

# MQTT settings
MQTT_SERVER_HOST = "192.168.0.17"
MQTT_SERVER_PORT = 1883
MQTT_SERVER_KEEPALIVE = 120
MQTT_TOPIC = "TeqBall"

# Display settings
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720

BACKGROUND_COLOR = (0, 0, 0)
BACKGROUND_LEFT = 0
BACKGROUND_TOP = -100

# Logging
LOG4P_CONFIG = "/home/pi/TeqBall/log4p.json"

# Fonts
FONT_FOLDER = "/home/pi/TeqBall/fonts/"

# Images
IMAGE_FOLDER = "/home/pi/TeqBall/images/"

# Scoreboard display settings
SCOREBOARD_TIME_FONT_TYPE = "OpenSans-Bold.ttf"
SCOREBOARD_TIME_FONT_SIZE = 160
SCOREBOARD_TIME_COLOR = (255, 215, 215)
SCOREBOARD_TIME_TOP = -20

SCOREBOARD_TEAM_FONT_TYPE = "OpenSans-CondBold.ttf"
SCOREBOARD_TEAM_FONT_SIZE = 100
SCOREBOARD_TEAM_1_COLOR = (255, 255, 255)
SCOREBOARD_TEAM_2_COLOR = (255, 255, 255)
SCOREBOARD_TEAM_TOP = DISPLAY_HEIGHT / 2 - 100
SCOREBOARD_TEAM_LEFT = 50

SCOREBOARD_TEAM_POINTS_FONT_TYPE = "OpenSans-CondBold.ttf"
SCOREBOARD_TEAM_POINTS_FONT_SIZE = 240
SCOREBOARD_TEAM_POINTS_LEFT = 50

SCOREBOARD_LABEL_FONT_TYPE = "DroidSansMono.ttf"
SCOREBOARD_LABEL_FONT_SIZE = 30
SCOREBOARD_LABEL_COLOR = (255, 255, 255)

# Hall of fame display settings
HOF_TITLE_FONT_TYPE = "OpenSans-Bold.ttf"
HOF_TITLE_FONT_SIZE = 200
HOF_TITLE_COLOR = (255, 255, 255)
HOF_TITLE_TOP = 0

HOF_ROW_FONT_TYPE = "OpenSans-Bold.ttf"
HOF_ROW_FONT_SIZE = 30
HOF_ROW_COLOR = (255, 255, 255)
HOW_ROW_TOP = 210

# Timing
MAIN_SLEEP = 0.01 # in seconds
GAMECLOCK_START_SECS = 5 * 60
HOF_CHANGE_INTERVAL_SECS = 5