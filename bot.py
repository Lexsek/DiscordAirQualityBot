import os
import discord
from discord.ext import commands

import locator

TOKEN=os.getenv("DISCORD_BOT_TOKEN")
PREFIX=os.getenv("DISCORD_BOT_PREFIX", default="~")
DEFAULT_CITY=os.getenv("DISCORD_DEFAULT_CITY", default="San Francisco")

purple = locator.PurpleSensorLocator()
bot = commands.Bot(command_prefix="~")

def mean(lst):
  try:
    return sum(lst) / len(lst)
  except ZeroDivisionError:
    return -1


@bot.command(description="describes the air quality for a location")
async def aqi(ctx, *where):
  location = " ".join(where) if where else DEFAULT_CITY
  sensor = purple.nearest_sensor(*locator.lookup_streetmap(location))
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
  sensor = purple.nearest_sensor(*locator.lookup_streetmap(location))
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
  lon, lat = locator.lookup_streetmap(location)
  pm25s = []
  temps = []
  humids = []
  press = []
  for pm in purple.nearest_sensors(lon, lat):
    pm25s.append(pm.parent.current_pm2_5)
    temps.append(pm.parent.current_temp_f)
    humids.append(pm.parent.current_humidity)
    press.append(pm.parent.current_pressure)
  meanpm25s = mean(pm25s)
  meanaqi, saying = locator.aqi_saying(meanpm25s)
  template = '''

See a map of the area
https://www.purpleair.com/map?opt=1/mAQI/a10/cC0#12/{}/{}

```
Average AQI:          {}
Average PM2.5         {:.2f}
Average Temperature:  {:.2f} F
Average Humidity:     {:.2F}
Average Pressure:     {:.2F}

The air quality is {}.

  * {}
```
'''

  await ctx.send(template.format(
    lat,
    lon,
    meanaqi,
    meanpm25s,
    mean(temps),
    mean(humids),
    mean(press),
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

