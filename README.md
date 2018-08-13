# DiscordAirQualityBot
A discord bot written in python in order to give air quality related informations given a city name in argument.

## Installation

First, you'll need the discord python libraries,<br>
`pip3 install discord --user`

Secondly, visit this url to create the application,<br>
`https://discordapp.com/developers/applications/`

(feel free to customize it's application name and it's image before saving changes)

Thirdly, you'll need to turn your application into a bot, by visiting this url and generating it's token,<br>
`https://discordapp.com/developers/applications/<client id>/bots`

Finally visit this page and configure permissions to get your adding link generated,<br>
`https://discordapi.com/permissions.html`

Here is an example :<br>
`https://discordapi.com/permissions.html#199680`<br>
`https://discordapp.com/oauth2/authorize?client\_id=INSERT\_CLIENT\_ID\_HERE&scope=bot&permissions=199680`

<b>WARNING : Don't forget to insert your bot token in the code.</b>
## Usage

Start the bot by running :<br>
`python pollutionbot.py`

If the bot has permission to read and send messages, just type :<br>
`!cancer City`

## Examples

15:37 Lexsek : !cancer Paris<br>
15:37 BOT Pollution :
```
City: Paris
Country: France
AQI: 73
Description: Good air quality
Recommendations:
 -Sport: You can go on a run - just keep your nose open for any changes!
 -Health: People with health sensitivities should monitor the air quality in the next few hours
 -Inside: The amount of pollutants in the air is noticeable, but still there is no danger to health - It is recommended to watch for changes
 -Outside: It's still OK to go out and enjoy a stroll, just pay attention for changes in air quality
```

15:37 Lexsek : !cancer monaco<br>
15:37 BOT Pollution :
```
City: monaco
Country: France
AQI: 70
Description: Good air quality
Recommendations:
 -Sport: You can go on a run - just keep your nose open for any changes!
 -Health: Exposure to air hazards is dangerous for people with health sensitivities, so it is important to monitor air quality at this time
 -Inside: The amount of pollutants in the air is noticeable, but still there is no danger to health - It is recommended to watch for changes
 -Outside: It's still OK to go out and enjoy a stroll, just pay attention for changes in air quality
```
# Future improvements
* Exception handling
* More parameters
* Other
