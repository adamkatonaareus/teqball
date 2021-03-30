/**

	Game clock controller
	(C) KA 2020

*/
/**
	Game clock controller.
*/
class GameClockController
{
	MODULE_NAME = "gameclock";

	//--- Fields
	config = new Config();
	client;


	/**
		Constructor
	*/
	constructor(client)
	{
		this.client = client;
		console.log("GameClockController created.");
	}

	/**
		Start the timer.
	*/
	start()
	{
		this.client.publish(MqttMessage.createCommand(this.MODULE_NAME, "start"));
	}

	/**
		Stop the timer.
	*/
	stop()
	{
		this.client.publish(MqttMessage.createCommand(this.MODULE_NAME, "stop"));
	}

	/**
		Reset the timer.
	*/
	reset()
	{
		this.client.publish(MqttMessage.createCommand(this.MODULE_NAME, "reset"));
	}

	/**
		Set timer to the given time in secs.
	*/
	setTime(time)
	{
		this.client.publish(MqttMessage.createCommand(this.MODULE_NAME, "settime", time));
	}

	onMessage(payload)
	{
		if (payload.module != this.MODULE_NAME)
			return;

		switch (payload.command)
		{
			case "settime":

				//--- Ignore our own message
				if (payload.isSync)
				{
					var minutes = payload.value.substr(0, 2);

					if (minutes < 1)
					{
						var seconds = Math.round(payload.value.substr(3, 7) * 10) / 10;
						document.getElementById('time').value = minutes + ":" + 
						(seconds < 10 ? "0" : "") + seconds +
						(seconds == Math.floor(seconds) ? ".0" : "");
					}
					else
					{
						var seconds = Math.floor(payload.value.substr(3, 7));
						document.getElementById('time').value = minutes + ":" + 
						(seconds < 10 ? "0" : "") + seconds;						
					}

				}

				break;
		}
	}	

}
