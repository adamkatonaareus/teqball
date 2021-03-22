
# MQTT client functions.
# (C) KA 2020

import config as CONFIG
import controller
import log4p
import paho.mqtt.client as mqtt
import socket
import json
import traceback


class MqttClient:

	log = None
	status = None
	client = None


	#
	# Constructor
	#
	def __init__(self, status):

		logger = log4p.GetLogger(__name__, config=CONFIG.LOG4P_CONFIG)
		self.log = logger.logger
		self.log.debug("Initializing MqttClient...")

		self.status = status


	def startup(self):

		self.log.info("Starting MqttClient...")
		self.client = mqtt.Client()
		self.client.on_connect = self.on_connect
		self.client.on_message = self.on_message
		self.client.on_disconnect = self.on_disconnect
		self.client.on_subscribe = self.on_subscribe
		self.connect()


	def shutdown(self):

		self.log.info("Shutting down MqttClient...")
		self.client.loop_stop()


	def connect(self):

		self.log.info("Connecting to " + CONFIG.MQTT_SERVER_HOST + ":" + str(CONFIG.MQTT_SERVER_PORT))
		self.client.connect_async(CONFIG.MQTT_SERVER_HOST, CONFIG.MQTT_SERVER_PORT, CONFIG.MQTT_SERVER_KEEPALIVE)
		self.client.loop_start()


	#
	# Process connection event.
	#
	def on_connect(self, client, userdata, flags, rc):

		self.log.info("Connected with result code "+str(rc))

		if (rc == 0):
			self.status.mqttConnected = True
			self.log.info("Subscribing to topic " + CONFIG.MQTT_TOPIC)
			client.subscribe(CONFIG.MQTT_TOPIC)
#			self.status.display.clear()
		else:
			self.status.mqttConnected = False

	#
	# Process disconnect event
	#
	def on_disconnect(self, client, userdata, rc):

		self.log.info("Disconnected from server. Code: "+str(rc))
		self.status.mqttConnected = False


	#
	# Process subscribe event
	#
	def on_subscribe(self, client, userdata, mid, granted_qos):

	    self.log.debug("Subscribed.")


	#
	# Process messages.
	#
	def on_message(self, client, userdata, msg):

		try:
			jsonString = msg.payload.decode("UTF-8")
			self.log.debug("Message received: " + msg.topic + " " + jsonString)

			message = json.loads(jsonString)

			# Do we need to stop?
			if ("module" in message and message["module"] == "settings" and message["command"] == "halt"):
				self.log.info("Halt message received, exiting...")
				self.status.isHalting = True
				return

			# Do we need to reset all? Controllers can respond to reset too, so we pass this on.
			if (message["command"] == "reset"):
				self.log.info("Reset message received, reseting...")
				self.status.reset()

			# Controllers can respond to ping too, so we pass this on.
			if (message["command"] == "ping"):
				self.log.debug("Ping message received...")
				self.ping()

			# Call controller to process message
			self.status.gameClockController.onMessage(message)
			self.status.mainController.onMessage(message)
		
		except Exception as e:

			self.log.error("Unexpected error: " + str(e))
			self.log.error(e)
			print(traceback.format_exc())


	#
	# Handle ping message.
	#
	def ping(self):

		hostname = socket.gethostname()    

		message =	{
			"command": "ping.back",
			"hostname": hostname,
			"moduleMode": CONFIG.CLIENT_MODE,
			"moduleId": CONFIG.CLIENT_ID
		}

		self.publish(message)

	#
	# Publish something.
	#
	def publish(self, message):

		self.client.publish(CONFIG.MQTT_TOPIC, json.dumps(message))

