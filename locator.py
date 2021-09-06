from datetime import datetime
from functools import lru_cache
from purpleair.network import SensorList, Sensor
import geopandas
import requests
import shapely
import logging
import aqi

class PurpleSensorLocator:
  def __init__(self):
    logging.info("initializing PurpleSensorLocator")
    self._updated = datetime.fromtimestamp(0)
    self.update()

  def __str__(self):
    # return "updated: %s, sensors: %d, gdf: %s" % (self._updated, len(self._sensors) if self._sensors else -1, self._gdf if self._gdf else "none")
    return "updated: %s" % self._updated
  
  # Update the dataframe if the cache was updated more than 6 hours ago.
  def update(self, cache_secs = 21600):
    logging.info("checking if PurpleSensorLocator information is out of date")
    now = datetime.now()
    since_updated = now - self._updated
    if since_updated.total_seconds() > cache_secs:
      logging.info("PurpleSensorLocator information is out of date")
      self._sensors = SensorList()
      df = self._sensors.to_dataframe(sensor_filter='useful', channel='parent')
      self._gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.lon, df.lat))
      self._updated = now
      logging.info("updated PurpleSensorLocator information")
    else:
      logging.info("PurpleSensorLocator is still up to date")
  
  def nearest_sensor(self, lon, lat):
    self.update()
    pt = shapely.ops.nearest_points(shapely.geometry.Point(lon, lat), self._gdf.geometry.unary_union)[1]
    series = self._gdf.geometry == pt
    rows = self._gdf.loc[series]
    # There will only be one row, really. Return a sensor with this index
    return Sensor(int(rows.index[0]), parse_location=True)

  def nearest_sensors(self, lon, lat, max_dist=50, max_num=5):
    self.update()
    logging.info("finding nearest points to %s, %s" % (lon, lat))
    yielded = 0
    distances = self._gdf.distance(shapely.geometry.Point(lon, lat)).sort_values()
    for sid, dist in distances.iteritems():
      if yielded > max_num or dist > max_dist:
        return
      yield Sensor(sid, parse_location=True)
      yielded += 1

@lru_cache(maxsize=100)
def lookup_streetmap(name):
  addr = "https://nominatim.openstreetmap.org/search/{}?format=json&limit=1".format(name)
  resp = requests.get(addr).json()
  return float(resp[0].get("lon")), float(resp[0].get("lat"))


# these sayings come from https://www.airnow.gov/sites/default/files/2021-03/air-quality-guide_pm_2015_0.pdf
sayings = [
  {
    "quality": "good",
    "concerned": "nobody",
    "do": [
      "It's a great day to be outside",
    ],
  },
  {
    "quality": "moderate",
    "concerned": "Some people who may be unusually sensitive to particle pollution.",
    "do": [ 
      "Unusually sensitive people: Consider reducing prolonged or heavy exertion. Watch for symptoms such as coughing or shortness of breath. These are signs to take it easier.",
      "Everyone else: It's a great day to be outside",
    ],
  },
  {
    "quality": "unhealthy for sensitive groups",
    "concerned": "Sensitive groups include people with heart or lung disease, older adults, children and teenagers.",
    "do": [
      "Sensitive groups: Reduce prolonged or heavy exertion. It’s OK to be active outside, but take more breaks and do less intense activities. Watch for symptoms such as coughing or shortness of breath.",
      "People with asthma should follow their asthma action plans and keep quick relief medicine handy.",
      "If you have heart disease: Symptoms such as palpitations, shortness of breath, or unusual fatigue may indicate a serious problem. If you have any of these, contact your heath care provider.",
    ],
  },
  {
    "quality": "unhealthy",
    "concerned": "everyone",
    "do": [
      "Sensitive groups: Avoid prolonged or heavy exertion. Consider moving activities indoors or rescheduling.",
      "Everyone else: Reduce prolonged or heavy exertion. Take more breaks during outdoor activities.",
    ],
  },
  {
    "quality": "very unhealthy",
    "concerned": "everyone",
    "do": [
      "Sensitive groups: Avoid all physical activity outdoors. Move activities indoors or reschedule to a time when air quality is better.",
      "Everyone else: Avoid prolonged or heavy exertion. Consider moving activities indoors or rescheduling to a time when air quality is better.",
    ]
  },
  {
    "quality": "hazardous",
    "concerned": "everyone",
    "do": [
      "Everyone: Avoid all physical activity outdoors.",
      "Sensitive groups: Remain indoors and keep activity levels low. Follow tips for keeping particle levels low indoors.",
    ]
  }
]


def aqi_saying(pm25):
  aq = aqi.to_aqi([(aqi.POLLUTANT_PM25, pm25)])
  if aq >= 301:
    saying = sayings[5]
  elif aq >= 201:
    saying = sayings[4]
  elif aq >= 151:
    saying = sayings[3]
  elif aq >= 101:
    saying = sayings[2]
  elif aq >= 51:
    saying = sayings[1]
  else:
    saying = sayings[0]

  return (aq, saying)
