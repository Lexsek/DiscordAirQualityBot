import requests

class Ville:

    def __init__(self, nom):
        self.nom = nom
        self.latitude = ""
        self.longitude = ""
        self.aqi = ""
        self.country = ""
        self.aqiDescription = ""
        self.recommendations = {
            "sport" : "",
            "health" : "",
            "inside" : "",
            "outside" : "",
        }

    def getCoordinates(self):
        response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address={}'.format(self.nom))
        resp_json_payload = response.json()
        self.latitude = resp_json_payload['results'][0]['geometry']['location']['lat']
        self.longitude = resp_json_payload['results'][0]['geometry']['location']['lng']

    def getInformations(self):
        headers = {
            'User-Agent' : 'Mozilla/5.0',
        }
        request = requests.get("https://api.breezometer.com/baqi/{0},{1}?key=4d92ed8a496d4ad6b7a85cf9a1f67292&debug=true".format(self.latitude, self.longitude))
        response = request.json()
        self.aqi = response["breezometer_aqi"]
        self.country = response["country_name"]
        self.aqiDescription = response["breezometer_description"]
        self.recommendations["sport"] = response["random_recommendations"]["sport"]
        self.recommendations["health"] = response["random_recommendations"]["health"] 
        self.recommendations["inside"] = response["random_recommendations"]["inside"]
        self.recommendations["outside"] = response["random_recommendations"]["outside"] 

    def formatInformations(self):
        self.getCoordinates()
        self.getInformations()
        return "```\nCity: {}\nCountry: {}\nAQI: {}\nDescription: {}\nRecommendations:\n -Sport: {}\n -Health: {}\n -Inside: {}\n -Outside: {}\n```".format(self.nom, self.country, self.aqi, self.aqiDescription, self.recommendations["sport"], self.recommendations["health"], self.recommendations["inside"], self.recommendations["outside"])
