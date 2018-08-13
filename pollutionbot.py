import discord
from pollution import *

TOKEN = 'INSERT_TOKEN_HERE'

client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!cancer'):
        try:
            msg = Ville(message.content[8:].lower()).formatInformations()
            await client.send_message(message.channel, msg)
        except:
            await client.send_message(message.channel, "Error occured, try again")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)
