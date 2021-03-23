/**

	Scoreboard controller
	(C) KA 2020

*/
/**
	Scoreboard controller.
*/
class ScoreBoardController
{
	MODULE_NAME = "scoreboard";

	//--- Fields
	config = new Config();
	client;


	/**
		Constructor
	*/
	constructor(client)
	{
		this.client = client;
		console.log("ScoreBoardController created.");
	}

	/**
		Set team name
	*/
	setTeamName(teamId)
	{
		var field = document.getElementById("team" + teamId);
		this.client.publish(MqttMessage.createCommand(this.MODULE_NAME, "setteamname").setTeamId(teamId).setValue(field.value));
	}

	/**
		Set player no.
	*/
	setPlayerNo(teamId, playerId)
	{
		var field = document.getElementById("playerNo" + teamId + "_" + playerId);
		this.client.publish(MqttMessage.createCommand(this.MODULE_NAME, "setplayerno").setTeamId(teamId).setPlayerId(playerId).setValue(Number(field.value)));
	}

	/**
		Set player name
	*/
	setPlayerName(teamId, playerId)
	{
		var field = document.getElementById("playerName" + teamId + "_" + playerId);
		this.client.publish(MqttMessage.createCommand(this.MODULE_NAME, "setplayername").setTeamId(teamId).setPlayerId(playerId).setValue(field.value));
	}

	/**
		Set player errors.
	*/
	setPlayerErrors(teamId, playerId)
	{
		var field = document.getElementById("playerErrors" + teamId + "_" + playerId);
		this.client.publish(MqttMessage.createCommand(this.MODULE_NAME, "setplayererrors").setTeamId(teamId).setPlayerId(playerId).setValue(Number(field.value)));
	}

	/**
		Set player points.
	*/
	setPlayerPoints(teamId, playerId)
	{
		var field = document.getElementById("playerPoints" + teamId + "_" + playerId);
		this.client.publish(MqttMessage.createCommand(this.MODULE_NAME, "setplayerpoints").setTeamId(teamId).setPlayerId(playerId).setValue(Number(field.value)));
	}	

	incPlayerPoints(teamId, playerId, addValue)
	{
		var field = document.getElementById("playerPoints" + teamId + "_" + playerId);
		field.value = Number(field.value) + addValue; 
		this.setPlayerPoints(teamId, playerId);
	}

	decPlayerPoints(teamId, playerId, decValue)
	{
		var field = document.getElementById("playerPoints" + teamId + "_" + playerId);

		if (field.value > 0)
		{
			field.value = Number(field.value) - decValue; 
			this.setPlayerPoints(teamId, playerId);
		}
	}	

	/**
		Set team points.
	*/
	setTeamPoints(teamId)
	{
		var field = document.getElementById("teamPoints" + teamId);
		this.client.publish(MqttMessage.createCommand(this.MODULE_NAME, "setteampoints").setTeamId(teamId).setValue(Number(field.value)));
	}	

	incTeamPoints(teamId, addValue)
	{
		var field = document.getElementById("teamPoints" + teamId);
		field.value = Number(field.value) + addValue; 
		this.setTeamPoints(teamId);
	}

	decTeamPoints(teamId, decValue)
	{
		var field = document.getElementById("teamPoints" + teamId);

		if (field.value > 0)
		{
			field.value = Number(field.value) - decValue; 
			this.setTeamPoints(teamId);
		}
	}	

	/**
		Set team errors.
	*/
	setTeamErrors(teamId)
	{
		var field = document.getElementById("teamErrors" + teamId);
		this.client.publish(MqttMessage.createCommand(this.MODULE_NAME, "setteamerrors").setTeamId(teamId).setValue(Number(field.value)));
	}	


	/**
		Set team timeouts
	*/
	setTimeouts(teamId)
	{
		var field = document.getElementById("timeouts" + teamId);
		this.client.publish(MqttMessage.createCommand(this.MODULE_NAME, "settimeouts").setTeamId(teamId).setValue(Number(field.value)));
	}	

	incTimeouts(teamId, addValue)
	{
		var field = document.getElementById("timeouts" + teamId);
		field.value = Number(field.value) + addValue; 
		this.setTimeouts(teamId);
	}

	decTimeouts(teamId, decValue)
	{
		var field = document.getElementById("timeouts" + teamId);
		if (field.value > 0)
		{
			field.value = Number(field.value) - decValue; 
			this.setTimeouts(teamId);
		}
	}

	/**
		Set winner
	*/
	setWin(teamId)
	{
		this.client.publish(MqttMessage.createCommand(this.MODULE_NAME, "setwin").setTeamId(teamId));
	}


	onMessage(payload)
	{
		if (payload.module != this.MODULE_NAME)
			return;

		switch (payload.command)
		{
			case "setboard":

				//--- Ignore our own message
				if (payload.isSync)
				{
					var field;

					//--- {"module": "scoreboard", "command": "setboard", "isSync": true, 
					//--- "teamName": ["Team 1", "Team 2"], "teamPoints": [123, 987], "teamErrors": [1, 2], "timeouts": [3, 0], "possession": 1, 
					//--- "playerNo": [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], [0, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]], 
					//--- "playerName": [["Kov\u00e1cs", "p1 2", "p1 3", "p1 4", "", "", "", "", "", "", "", "p1 12"], 
					//--- ["p2 1", "p2 2", "", "", "", "", "", "", "", "", "", "p2 12"]], 
					//--- "playerErrors": [[0, 1, 2, 3, 4, 5, 0, 0, 0, 0, 0, 0], [0, 0, 3, 1, 5, 2, 0, 4, 0, 0, 0, 0]], 
					//--- "playerPoints": [[0, 10, 0, 0, 20, 0, 0, 5, 0, 0, 0, 0], [2, 0, 0, 10, 0, 20, 0, 0, 5, 0, 0, 0]]}

					document.getElementById("team1").value = payload.teamName[0];
					document.getElementById("team2").value = payload.teamName[1];

					document.getElementById("teamPoints1").value = payload.teamPoints[0];
					document.getElementById("teamPoints2").value = payload.teamPoints[1];			
				}

				break;
		}
	}	
}
