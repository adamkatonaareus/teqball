/**

	Settings controller
	(C) KA 2020

*/
/**
	Settings controller.
*/
class SettingsController
{
	MODULE_NAME = "settings";

	//--- Fields
	config = new Config();
	client;


	/**
		Constructor
	*/
	constructor(client)
	{
		this.client = client;
		console.log("SettingsController created.");
	}

	/**
		Shut down the system.
	*/
	halt()
	{
		if (confirm("Do you really want to stop the display?"))
		{
			this.client.publish(MqttMessage.createCommand(this.MODULE_NAME, "halt"));
		}
	}

	/**
		Reset the system.
	*/
	reset()
	{
		if (confirm("Do you really want to reset the display?"))
		{
			//--- KA: reset goes to all modules.
			this.client.publish(MqttMessage.createCommand("", "reset"));
		}
	}

	onMessage(payload)
	{
		switch (payload.command)
		{
			case "ping.back":
				var control = document.getElementById('pingBack');
				control.innerText += "Module: " + payload.hostname + " online, id: " + payload.moduleId + "\r\n";
		}
	}

}
