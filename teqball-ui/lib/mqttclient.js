/**
	 MQTT Client
 	(C) KA 2020
*/

var controllers = new Array();

/**
	Mqtt client.
*/
class MqttClient
{
	//--- Fields
	config = new Config();
	client;
	

	/**
		Constructor
	*/
	constructor()
	{

	}


	/**
		Start the client.
	*/
	startup()
	{
		console.log("Starting MqttClient...");

		//TODO: error handling.
        this.client = mqtt.connect(this.config.MQTT_SERVER_URL);
        this.client.subscribe(this.config.MQTT_TOPIC);

        this.client.on("message", this.onMessage);
      	
      	this.ping();

        console.log("MqttClient started.");
	}


	/**
		Shut down the client.
	*/
	shutdown()
	{
		this.client.end();
	}


	/**
		Publish a command.
	*/
	publish(message)
	{
		this.client.publish(this.config.MQTT_TOPIC, JSON.stringify(message));
	}


	/**
		Publish a ping command so displays respond.
	*/
	ping()
	{
		this.publish(MqttMessage.createCommand("", "ping"));
	}

	/**
		Add a controller.
	*/
	addController(controller)
	{
		controllers.push(controller);
	}

	/**
		MQTT message received.
	*/
	onMessage(topic, payload)
	{
		console.log(topic + ": " + payload);
	
		var message = JSON.parse(new TextDecoder("utf-8").decode(payload));

		controllers.forEach(controller => controller.onMessage(message));
	}

}

