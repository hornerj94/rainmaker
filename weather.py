import requests

def getWeatherData(city):
#------------------------------------------------------------------------------

    api_key = "bc6351bf115e5384ff7a8e9c1525b758"
    base_url = "http://api.openweathermap.org/data/2.5/weather?lang=de"
    final_url = base_url + "appid=" + api_key + "&q=" + city + "&units=metric"

    weather_data = requests.get(final_url).json()
        
    return weather_data
#------------------------------------------------------------------------------