import os
import discord
from discord.ext import commands

import aqi as aqimod

TOKEN=os.getenv("DISCORD_BOT_TOKEN")
PREFIX=os.getenv("DISCORD_BOT_PREFIX", default="~")
DEFAULT_CITY=os.getenv("DISCORD_DEFAULT_CITY", default="San Francisco")

purple = aqimod.PurpleSensorLocator()
bot = commands.Bot(command_prefix="~")

@bot.command(description="describes the air quality for a location")
async def aqi(ctx, *where):
  location = " ".join(where) if where else DEFAULT_CITY
  sensor = purple.nearest_sensor(*aqimod.lookup_streetmap(location))
  template = '''
Weather information provided by purpleair.com
```
Location: {} ({}, {})
Temperature: {}
Pressure: {}
Humidity: {}
pm2.5: {}
```
'''
  await ctx.send(template.format(
    sensor.location,
    sensor.parent.lon,
    sensor.parent.lat,
    sensor.parent.current_temp_f,
    sensor.parent.current_pressure,
    sensor.parent.current_humidity,
    sensor.parent.current_pm2_5_atm))


@bot.command(description="historical data for a location")
async def aqihist(ctx, *where):
  location = " ".join(where) if where else DEFAULT_CITY
  sensor = purple.nearest_sensor(*aqimod.lookup_streetmap(location))
  rows = sensor.parent.get_historical(1, "primary")
  template = '''
```
{}
```
'''
  message = template.format(rows.head(5).to_markdown())
  await ctx.send(message)

@bot.command(description="air quality")
async def air(ctx, *where):
  location = " ".join(where) if where else DEFAULT_CITY
  lon, lat = aqimod.lookup_streetmap(location)
  pms = {}
  for pm in purple.nearest_sensors(lon, lat):
    pms[pm.location] = pm.parent.current_pm2_5_atm
  meanaqi = sum(pms.values()) / len(pms)
  aqi, saying = aqimod.aqi_saying(meanaqi)
  template = '''
```
PM2.5 for the sensors near you:
  * {}

Average AQI: {}

The air quality is {}.

  * {}
```
'''

  await ctx.send(template.format(
    "\n  * ".join([": ".join([k, str(v)]) for k, v in pms.items()]),
    meanaqi,
    saying.get("quality"),
    "\n  * ".join(saying.get("do")),
  ))

# @bot.command(description="debug")
# async def debug(ctx):
#   await ctx.send(purple)

# @bot.command(description="debug")
# async def update(ctx):
#   purple.update()
#   await ctx.send(purple)

bot.run(TOKEN)
