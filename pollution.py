import requests
import json


class Ville:

    def __init__(self, nom):
        self.nom = nom
        self.latitude = ""
        self.longitude = ""
        self.aqi = ""
        self.country = ""
        self.aqiDescription = ""
        self.recommendations = {
            "sport": "",
            "health": "",
            "inside": "",
            "outside": "",
        }

    def get_coordinates(self):
        addr = 'https://nominatim.openstreetmap.org/search/{}?format=json&limit=1'.format(
            self.nom)
        response = json.loads(requests.get(addr).content)
        self.latitude = response[0]["lat"]
        self.longitude = response[0]["lon"]

    def get_informations(self):
        request = requests.get(
            "https://api.breezometer.com/baqi/{0},{1}?key=4d92ed8a496d4ad6b7a85cf9a1f67292&debug=true".format(
                self.latitude, self.longitude))
        response = request.json()
        self.aqi = response["breezometer_aqi"]
        self.country = response["country_name"]
        self.aqiDescription = response["breezometer_description"]
        self.recommendations["sport"] = response["random_recommendations"]["sport"]
        self.recommendations["health"] = response["random_recommendations"]["health"]
        self.recommendations["inside"] = response["random_recommendations"]["inside"]
        self.recommendations["outside"] = response["random_recommendations"]["outside"]

    def format_informations(self):
        self.get_coordinates()
        self.get_informations()
        msg = '''
```
City: {}
Country: {}
AQI: {}
Description: {}
Recommendations:
    -Sport: {}
    -Health: {}
    -Inside: {}
    -Outside: {}
```
'''.format(
    self.nom,
    self.country,
    self.aqi,
    self.aqiDescription,
    self.recommendations["sport"],
    self.recommendations["health"],
    self.recommendations["inside"],
    self.recommendations["outside"])
        return msg
