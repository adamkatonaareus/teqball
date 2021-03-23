/**

	JSON mqtt message used for communication
	(C) KA 2020

*/

class MqttMessage
{
	module;
	moduleId;
	command;
	teamId;
	playerId;
	value;
	isSync;

	// constructor(module)
	// {
	// 	this.module = module;
	// }



	constructor(module, moduleId, command)
	{
		this.module = module;
		this.moduleId = moduleId;
		this.command = command;
	}

	static createCommand(module, command, value)
	{
		var message = new MqttMessage(module);
		message.command = command;
		message.value = value;
		return message;
	}

	setTeamId(teamId)
	{
		this.teamId = teamId;
		return this;
	}

	setPlayerId(playerId)
	{
		this.playerId = playerId;
		return this;
	}

	setValue(value)
	{
		this.value = value;
		return this;
	}
}