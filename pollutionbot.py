import os
import sys
import logging

import discord

from pollution import *

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
NAME = os.getenv('BOT_NAME', default='!aqi')
DEFAULT_CITY = os.getenv('DEFAULT_CITY', default='San Francisco')


client = discord.Client()


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    channel = message.channel
    if message.content.startswith(NAME):
        city = ' '.join(message.content.split(' ')[1:])
        try:
            msg = Ville(city or DEFAULT_CITY).format_informations()
        except BaseException:
            logging.warn('error retreiving information:', exc_info=sys.exc_info())
        try:
            await channel.send(msg)
        except BaseException:
            logging.warn('error sending to channel:', exc_info=sys.exc_info())


@client.event
async def on_ready():
    logging.info('We have logged in as {0.user}'.format(client))


if not TOKEN:
    logging.fatal('need token. Set DISCORD_BOT_TOKEN.')
    sys.exit(1)

client.run(TOKEN)
